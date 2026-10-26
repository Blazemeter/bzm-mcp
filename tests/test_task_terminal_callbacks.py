"""
Copyright 2025 Perforce Software, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import asyncio

import tools.async_task_manager as task_manager
from models.result import BaseResult


def test_callback_runs_when_the_task_finishes(session_scope):
    async def scenario():
        fired = []

        async def work():
            await asyncio.sleep(0.02)
            return BaseResult(result=["ok"])

        task_id = await task_manager.submit_task({"method": "work"}, work, scope=session_scope)
        await task_manager.add_task_terminal_callback(task_id, session_scope, lambda: _record(fired))
        assert fired == []
        record = await task_manager.get_task_record(task_id, scope=session_scope)
        await record.asyncio_task
        assert fired == ["fired"]
        assert task_manager._terminal_callbacks == {}

    asyncio.run(scenario())


def test_callback_runs_immediately_for_unknown_task(session_scope):
    async def scenario():
        fired = []
        await task_manager.add_task_terminal_callback("missing1", session_scope, lambda: _record(fired))
        assert fired == ["fired"]

    asyncio.run(scenario())


def test_callbacks_drain_when_the_runner_fails_before_running(monkeypatch, session_scope):
    real_persist = task_manager._set_status_and_persist
    failures = {"parking": 0}

    async def flaky_persist(record, status, message):
        if status == task_manager.STATUS_PARKING and not failures["parking"]:
            failures["parking"] += 1
            raise RuntimeError("storage unavailable")
        await real_persist(record, status, message)

    monkeypatch.setattr(task_manager, "_set_status_and_persist", flaky_persist)

    async def scenario():
        fired = []

        async def work():
            return BaseResult(result=["never"])

        task_id = await task_manager.submit_task({"method": "work"}, work, scope=session_scope)
        # Registered before the runner gets a chance to start.
        await task_manager.add_task_terminal_callback(task_id, session_scope, lambda: _record(fired))
        record = await task_manager.get_task_record(task_id, scope=session_scope)
        await record.asyncio_task
        assert failures["parking"] == 1
        assert record.status == task_manager.STATUS_FAILED
        assert fired == ["fired"]
        assert task_manager._terminal_callbacks == {}

    asyncio.run(scenario())


async def _record(fired):
    fired.append("fired")
