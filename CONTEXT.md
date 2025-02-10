# Task Management API with AI Assistance

## Project Overview

This is a FastAPI-based backend service that uses AI (OpenAI and CrewAI) to assist in task management. The system helps
with task descriptions, duration estimates, and assignee matching.

## Core Features

### 1. Task Description Generation

- Endpoint: `/suggest-description`
- Automatically generates detailed task descriptions from titles
- Uses OpenAI GPT-3.5 to create comprehensive descriptions including:
  - Main objective
  - Key requirements
  - Expected outcomes

### 2. Task Duration Estimation

- Endpoint: `/suggest-duration`
- Estimates task completion time based on:
  - Task title and description
  - Assignee's skills (if provided)
  - Current workload
- Provides formatted durations (minutes/hours/days) with explanations

### 3. Assignee Matching System

- Endpoint: `/assignee-candidates`
- Uses a crew of AI agents to match tasks with suitable team members
- Three-step analysis process:
  1. Task Analysis: Identifies required skills and expertise level
  2. User Profiling: Matches user skills against requirements
  3. Workload Analysis: Considers current task load and priorities

## Technical Architecture

### AI Components

1. **OpenAI Integration**

   - Direct GPT-3.5 integration for task descriptions and duration estimates
   - Structured prompt engineering for consistent outputs

2. **CrewAI System**
   - Multiple specialized AI agents working together
   - Agents:
     - Task Analyzer
     - User Profiler
     - Workload Analyzer

### Data Models

1. **Task-Related Models**

   - TaskData: Core task information
   - TaskDescriptionRequest/Response
   - TaskDurationRequest/Response

2. **User-Related Models**
   - UserProfile: User information and skills
   - UserTask: Task assignments
   - UserSuggestion: AI recommendations

### Configuration

- YAML-based configuration for:
  - AI agents' roles and behaviors
  - Task analysis parameters
  - System workflows

## Project Structure
