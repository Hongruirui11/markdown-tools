import streamlit as st
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts'))

from markdown_converter import MarkdownToDocxConverter

st.set_page_config(
    page_title="Markdown 转 Word",
    page_icon="📄",
    layout="centered"
)

st.title("📄 Markdown 转 Word 转换器")
st.markdown("---")

DEFAULT_TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'assets', 'word-template.docx')

st.markdown('<style>h3 { font-size: 1.1rem !important; }</style>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 1. 上传 Markdown 文件")
    md_file = st.file_uploader(
        "选择 .md 文件",
        type=['md', 'markdown'],
        help="上传需要转换的 Markdown 文件"
    )

with col2:
    st.markdown("### 2. 上传 Word 模板（可选）")
    template_file = st.file_uploader(
        "选择 .docx 模板文件",
        type=['docx'],
        help="可选：上传自定义 Word 模板，不传则使用默认模板"
    )

st.markdown("---")

if st.button("开始转换", type="primary", disabled=not md_file):
    with st.spinner("正在转换..."):
        try:
            temp_md_path = os.path.join(os.path.dirname(__file__), 'temp_input.md')
            with open(temp_md_path, 'wb') as f:
                f.write(md_file.getvalue())

            output_filename = os.path.splitext(md_file.name)[0] + '.docx'
            output_path = os.path.join(os.path.dirname(__file__), output_filename)

            template_path = None
            if template_file:
                temp_template_path = os.path.join(os.path.dirname(__file__), 'temp_template.docx')
                with open(temp_template_path, 'wb') as f:
                    f.write(template_file.getvalue())
                template_path = temp_template_path
                st.info(f"使用自定义模板: {template_file.name}")
            else:
                if os.path.exists(DEFAULT_TEMPLATE_PATH):
                    template_path = DEFAULT_TEMPLATE_PATH
                    st.info("使用默认模板: word-template.docx")
                else:
                    st.warning("未找到默认模板，将使用空白文档")

            converter = MarkdownToDocxConverter(temp_md_path, output_path, template_path)
            converter.convert_file()

            with open(output_path, 'rb') as f:
                st.download_button(
                    label="📥 下载 Word 文件",
                    data=f.read(),
                    file_name=output_filename,
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )

            os.remove(temp_md_path)
            if template_file and os.path.exists(temp_template_path):
                os.remove(temp_template_path)
            if os.path.exists(output_path):
                os.remove(output_path)

            st.success("转换成功！")

        except Exception as e:
            st.error(f"转换失败: {str(e)}")

st.markdown("---")
st.caption("支持 Markdown 语法：标题、段落、列表、表格、代码块等")
