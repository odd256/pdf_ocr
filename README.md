# PDF OCR

这是一个专为“非常规、非标长文档”设计的 PDF 结构化数据提取工具。它不再依赖固定的正则或模板，而是通过 **LLM (大语言模型)** 和 **动态字段配置引擎**，将复杂的 PDF 报告、合同、审计表等直接转化为精准的 JSONL 结构化数据。

## 🌟 核心特性

- **规则驱动的分段提取**：支持在 `config.toml` 中按页码（如 `page = 3`）或页码范围（如 `page = "9-16"`) 定义独立的提取规则，各段逻辑互不干扰。
- **多模态解析支持**：
    - **`text` 类型**：针对文字密集型页面，提取核心语义字段。
    - **`table` 类型**：针对表格密集型页面，精准还原行列关系并转为结构化字典。
- **纯配置化字段定制**：无需修改任何 Python 代码，通过配置文件即可定义字段列表及字段描述（Description），自动生成 JSON Schema 引导 AI。
- **视觉 fallback 机制**：内置 OCR 兜底（pdf2image + Tesseract），确保扫描件文档也能准确识别。
- **企业级批处理**：支持大规模目录扫描、自动重试、大模型响应清洗及进度条跟踪。

## 🛠️ 环境要求

- **Python 3.11+**
- **[uv](https://github.com/astral-sh/uv)** (推荐的极速包管理工具)
- **系统依赖**：
  - [Poppler](https://poppler.freedesktop.org/) (PDF 转图片支持)
  - [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) (扫描件识别 fallback)

## 🚀 快速上手

### 1. 安装依赖
```bash
uv sync 
```

### 2. 配置你的提取规则
拷贝 `config.toml.example` 为 `config.toml` 并编辑：

```toml
[paths]
input_folder = "./pdfs"           # PDF 所在目录
output_file = "./output/res.jsonl" # 结果保存路径

[llm]
base_url = "http://localhost:11434/v1" # OpenAI 兼容接口
api_key = "sk-xxxx"                    # API Key
model = "qwen2.5-7b-instruct"          # 模型名称

[processing]
# -- 第 1 个提取块：首页基础信息 --
[[processing.pages]]
page = 1
type = "text"
fields = ["公司名称", "订单编号", "日期"]

# -- 第 2 个提取块：中间段落详细描述 --
[[processing.pages]]
page = "2-5"
type = "text"
fields = [
    { name = "风险项", description = "提取第2至第5页中提到的所有风险等级，填入：大/中/小" },
    { name = "建议措施", description = "针对每个风险给出的改进方案" }
]

# -- 第 3 个提取块：末尾费用明细表 --
[[processing.pages]]
page = 10
type = "table"
fields = ["明细项", "单价", "数量", "总额"]
```

### 3. 运行程序
准备好 PDF 文件后，直接执行：
```bash
uv run main.py
```
程序将自动扫描 `input_folder` 中的所有 PDF，按定义的规则分层提取并将最终结果聚合到 `output.jsonl` 中。

## 📁 项目结构
- `main.py`: 项目入口，加载配置并分发任务。
- `src/batch_runner.py`: 负责 PDF 文件扫描、页码切分与并发调度。
- `src/pdf_processor.py`: PDF 解析核心，集成 pdfplumber 提取与 Tesseract OCR 视觉 fallback。
- `src/llm_extractor.py`: 负责 Prompt 构建、JSON Schema 生成及 LLM 交互。
- `config.toml`: 全局唯一的规则配置中心。

## 📄 开源协议
本项目采用 [MIT License](LICENSE) 开源协议。
