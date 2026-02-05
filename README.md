# MCP CDS Server

MCP server cung cấp các tools cho hệ thống CDS (Clinical Data System) thông qua Model Context Protocol. Server này hoạt động như một proxy, nhận tool calls từ MCP client và chuyển tiếp đến CDS backend APIs để xử lý.

## Architecture

```
MCP Client/LLM
    ↓
MCP Server (this project)
    ↓
CDS Backend APIs
    ↓
OpenAI API + Database
```

## Prerequisites

- Python 3.11+
- pip hoặc uv (package manager)
- CDS backend server running (server at `http://localhost:8000` by default)
- OpenAI API key

## Installation

### 1. Clone Repository
```bash
git clone <repository-url>
cd new_project
```

### 2. Install Dependencies

**Option A: Using pip**
```bash
pip install -r requirements.txt
```

**Option B: Using uv (faster)**
```bash
uv pip install -r requirements.txt
```

Hoặc cài đặt từ `pyproject.toml`:
```bash
pip install -e .
```

### 3. Setup Environment Variables

Tạo file `.env` trong thư mục project:

```env
# CDS Backend Configuration
CDS_API_BASE_URL=http://localhost:8000

# OpenAI Configuration (nếu backend không có)
OPENAI_API_KEY=sk-your-openai-api-key
```

## Running the Server

### Start MCP Server

```bash
python main.py
```

Hoặc với uvicorn (nếu là async server):
```bash
uvicorn main:app --reload
```

### Verify Server is Running

Server sẽ khởi động và chờ MCP client kết nối. Output sẽ tương tự:

```
MCP Server starting...
Listening for MCP client connections on stdio
Available tools:
  - laboratory_test: Extract laboratory test values from documents
  - generate_crf: Generate CRF form from attachment
```