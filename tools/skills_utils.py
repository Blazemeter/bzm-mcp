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
import os
import re
from pathlib import Path
from typing import Tuple, Dict, List

from config.blazemeter import TOOLS_PREFIX
from tools.utils import get_resources_path

SKILL_PREFIX = f"{TOOLS_PREFIX}-skill-"
SKILL_URI_REGEX = re.compile(rf"^{SKILL_PREFIX}(?P<skill_name>[a-zA-Z0-9_-]+)://(?P<path>.+)$")


def parse_frontmatter(frontmatter: str) -> Dict[str, str]:
    meta = {}
    lines = frontmatter.splitlines()
    current_key = None
    current_value = []
    block_mode = False

    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            continue  # Skip empty or comment lines

        if ':' in line and not line.startswith((' ', '\t')):  # New key at root level
            if current_key:
                value_str = '\n'.join(current_value).strip()
                value_str = str(value_str).strip('\'"')  # Strip outer quotes if present
                meta[current_key] = value_str
            try:
                key, value = [part.strip() for part in line.split(':', 1)]
                value = str(value).strip('\'"')  # Strip quotes from single-line value
            except ValueError:
                raise ValueError("Invalid key-value format in frontmatter")

            if key not in ('name', 'description'):
                continue  # Ignore unexpected keys

            if value in ('|', '>'):
                block_mode = True
                current_value = []
            else:
                block_mode = False
                current_value = [value]

            current_key = key
        elif current_key and (block_mode or line.startswith((' ', '\t'))):
            # Append to multi-line block (indented or in block mode)
            current_value.append(line.rstrip() if block_mode else line.strip())
        else:
            raise ValueError("Malformed frontmatter structure")

    if current_key:
        value_str = '\n'.join(current_value).strip()
        value_str = value_str.strip('\'"')  # Strip outer quotes if present
        meta[current_key] = value_str

    # Ensure required keys are present after parsing
    if 'name' not in meta or 'description' not in meta:
        raise ValueError("Missing 'name' or 'description' in frontmatter")

    return meta


def list_skills() -> Tuple[List[Dict], List[str]]:
    full_skills_dir = os.path.join(get_resources_path(), 'skills')
    skills = []
    errors = []
    skills_path = Path(full_skills_dir)

    if not os.path.exists(skills_path):
        # Graceful handling
        return [], [f"Missing skills directory: {skills_path}"]

    for folder in os.listdir(skills_path):
        folder_path = skills_path / folder
        if folder_path.is_dir():
            md_path = folder_path / 'SKILL.md'
            if md_path.exists():
                skill, error = read_skill_meta(md_path)
                if skill is not None:
                    skills.append(skill)
                if error is not None:
                    errors.append(error)
            else:
                errors.append(f"Skill file not found: {md_path}")
        else:
            errors.append(f"Invalid Skill folder {folder_path}")
    return skills, errors


def validate_skill_content(content, md_path):
    if not content.startswith('---'):
        return False, "No YAML frontmatter found"

    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format"

    frontmatter = match.group(1)

    if 'name:' not in frontmatter:
        return False, "Missing 'name' in frontmatter"
    if 'description:' not in frontmatter:
        return False, "Missing 'description' in frontmatter"

    try:
        meta = parse_frontmatter(frontmatter)
        name = meta.get('name')
        description = meta.get('description')

        if not name or not description:
            return False, "Name or description is empty"

        # Validate name: hyphen-case
        if not re.match(r'^[a-z0-9-]+$', name):
            return False, f"Name '{name}' should be hyphen-case (lowercase letters, digits, and hyphens only)"
        if name.startswith('-') or name.endswith('-') or '--' in name:
            return False, f"Name '{name}' cannot start/end with hyphen or contain consecutive hyphens"

        # Validate description: no angle brackets
        if '<' in description or '>' in description:
            return False, "Description cannot contain angle brackets (< or >)"

    except ValueError as e:
        return False, f"Error parsing frontmatter in {md_path}: {str(e)}"

    return True, "Skill is valid"


def read_skill_meta(md_path) -> Tuple[Dict[str, None], str | None]:
    skill = None
    error = None
    content = md_path.read_text(encoding='utf-8')
    valid, message = validate_skill_content(content, md_path)
    if valid:
        match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if match:
            frontmatter = match.group(1)
            try:
                meta = parse_frontmatter(frontmatter)
                name = meta.get('name')
                description = meta.get('description')
                if name and description:
                    skill = {
                        'name': name,
                        'description': description
                    }
            except ValueError as e:
                error = f"Error parsing frontmatter in {md_path}: {str(e)}"
    else:
        error = f"Validation failed for {md_path}: {message}"
    return skill, error


def get_skill_file_path(skill_name: str, file_path: str) -> Path:
    fixed_file_path = file_path.split("#")[0]  # Protection against the use of anchors
    full_skills_dir = os.path.join(get_resources_path(), 'skills')
    skills_path = Path(full_skills_dir)
    return skills_path / skill_name / fixed_file_path


def replace_skills_markdown_links(content: str, skill_name: str, file_path: str) -> str:
    # Markdown Link Pattern []()
    pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

    def replacer(match):
        text, url = match.groups()
        # Detect when not it's a protocol link
        if not re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*://', url):
            # Only when it's relative to local, generate the uri format
            # Transform the relative path to absolute and cut the base path
            skills_path = Path(os.path.join(get_resources_path(), 'skills'))
            base_path = skills_path / skill_name / file_path
            url = (base_path.parent / url).resolve()
            try:
                url = url.relative_to(skills_path / skill_name).as_posix()
                new_url = f"{SKILL_PREFIX}{skill_name}://{url}"
                return f"[{text}]({new_url})"
            except:
                return match.group(0)  # In case the relative not it's valid, use the original
        else:
            # The MCP to don't allow collision replace generic global skill with prefixed
            new_url = url
            if url.split("://")[0].startswith('skill-'):
                new_url = url.replace("skill-", f"{SKILL_PREFIX}")
            return f"[{text}]({new_url})"

    return pattern.sub(replacer, content)


def read_skill_file(skill_name: str, file_path: str) -> Tuple[str | None, str | None]:
    skill_file_path = get_skill_file_path(skill_name, file_path)
    if skill_file_path.exists():
        content = skill_file_path.read_text(encoding='utf-8')
        if file_path.endswith('.md'):  # Only on Markdown replace to skills uri format
            content = replace_skills_markdown_links(content, skill_name, file_path)
        if file_path.endswith('SKILL.md'):
            valid, message = validate_skill_content(content, file_path)
            if valid:
                return content, None
            else:
                return None, f"Validation failed for {skill_name}: {message}"
        else:
            return content, None
    else:
        return None, f"Skill file not found: {skill_file_path}"


def is_skill_uri(uri: str) -> bool:
    return bool(SKILL_URI_REGEX.match(uri))


def parse_skill_uri(uri: str) -> Tuple[str, str]:
    match = SKILL_URI_REGEX.match(uri)
    if not match:
        raise ValueError(f"Invalid Skill URI : {uri}")
    return match.group("skill_name"), match.group("path")


def list_skill_resources_uri(skill_name: str) -> List[str]:
    full_skills_dir = os.path.join(get_resources_path(), 'skills')
    skills_path = Path(full_skills_dir)
    skill_path = skills_path / skill_name
    skill_resources = []
    for file_path in skill_path.rglob("*"):
        if file_path.is_file():
            url = file_path.relative_to(skills_path / skill_name).as_posix()
            skill_resources.append(f"{SKILL_PREFIX}{skill_name}://{url}")
    return skill_resources


def read_skill_definition(skill_name: str) -> Tuple[str | None, str | None]:
    return read_skill_file(skill_name, 'SKILL.md')
