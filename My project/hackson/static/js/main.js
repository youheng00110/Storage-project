/**
 * 首页主要 JavaScript
 */

// 模型配置
const MODELS = {
    modelscope: [
        { id: 'Qwen/Qwen2.5-72B-Instruct', name: 'Qwen2.5-72B (推荐)' },
        { id: 'Qwen/Qwen2.5-32B-Instruct', name: 'Qwen2.5-32B' },
        { id: 'Qwen/Qwen2.5-Coder-32B-Instruct', name: 'Qwen2.5-Coder-32B' },
        { id: 'Qwen/Qwen2.5-14B-Instruct', name: 'Qwen2.5-14B (快速)' }
    ],
    openai: [
        { id: 'gpt-4o', name: 'GPT-4o (推荐)' },
        { id: 'gpt-4o-mini', name: 'GPT-4o Mini (快速)' },
        { id: 'gpt-4-turbo', name: 'GPT-4 Turbo' },
        { id: 'gpt-3.5-turbo', name: 'GPT-3.5 Turbo (经济)' }
    ],
    qianwen: [
        { id: 'qwen-max', name: '通义千问 Max (推荐)' },
        { id: 'qwen-plus', name: '通义千问 Plus' },
        { id: 'qwen-turbo', name: '通义千问 Turbo (快速)' }
    ],
    claude: [
        { id: 'claude-3-5-sonnet-20241022', name: 'Claude 3.5 Sonnet (推荐)' },
        { id: 'claude-3-opus-20240229', name: 'Claude 3 Opus (高质量)' },
        { id: 'claude-3-haiku-20240307', name: 'Claude 3 Haiku (快速)' }
    ]
};

// DOM 元素
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const fileSize = document.getElementById('fileSize');
const removeFile = document.getElementById('removeFile');
const providerSelect = document.getElementById('provider');
const modelSelect = document.getElementById('model');
const apiKeyInput = document.getElementById('apiKey');
const toggleKey = document.getElementById('toggleKey');
const submitBtn = document.getElementById('submitBtn');
const uploadForm = document.getElementById('uploadForm');

// 状态
let selectedFile = null;
let uploadedFileId = null;

// 初始化
function init() {
    setupUploadArea();
    setupProviderSelect();
    setupApiKeyToggle();
    setupFormSubmit();
    checkFormValidity();
}

// 设置上传区域
function setupUploadArea() {
    // 点击上传
    uploadArea.addEventListener('click', () => fileInput.click());
    
    // 文件选择
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileSelect(e.target.files[0]);
        }
    });
    
    // 拖拽上传
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });
    
    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });
    
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        
        if (e.dataTransfer.files.length > 0) {
            handleFileSelect(e.dataTransfer.files[0]);
        }
    });
    
    // 移除文件
    removeFile.addEventListener('click', (e) => {
        e.stopPropagation();
        clearFile();
    });
}

// 处理文件选择
function handleFileSelect(file) {
    const allowedTypes = ['.pdf', '.docx', '.md', '.markdown', '.txt'];
    const ext = '.' + file.name.split('.').pop().toLowerCase();
    
    if (!allowedTypes.includes(ext)) {
        alert('不支持的文件类型。请上传 PDF、Word 或 Markdown 文件。');
        return;
    }
    
    if (file.size > 20 * 1024 * 1024) {
        alert('文件大小超过 20MB 限制。');
        return;
    }
    
    selectedFile = file;
    uploadedFileId = null;
    
    // 显示文件信息
    fileName.textContent = file.name;
    fileSize.textContent = formatFileSize(file.size);
    uploadArea.style.display = 'none';
    fileInfo.style.display = 'flex';
    
    checkFormValidity();
}

// 清除文件
function clearFile() {
    selectedFile = null;
    uploadedFileId = null;
    fileInput.value = '';
    uploadArea.style.display = 'block';
    fileInfo.style.display = 'none';
    checkFormValidity();
}

// 格式化文件大小
function formatFileSize(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
}

// 设置服务商选择
function setupProviderSelect() {
    providerSelect.addEventListener('change', () => {
        const provider = providerSelect.value;
        
        modelSelect.innerHTML = '';
        
        if (provider && MODELS[provider]) {
            modelSelect.disabled = false;
            MODELS[provider].forEach((model, index) => {
                const option = document.createElement('option');
                option.value = model.id;
                option.textContent = model.name;
                if (index === 0) option.selected = true;
                modelSelect.appendChild(option);
            });
        } else {
            modelSelect.disabled = true;
            const option = document.createElement('option');
            option.textContent = '请先选择服务商';
            modelSelect.appendChild(option);
        }
        
        checkFormValidity();
    });
}

// 设置 API Key 显示/隐藏
function setupApiKeyToggle() {
    toggleKey.addEventListener('click', () => {
        const type = apiKeyInput.type === 'password' ? 'text' : 'password';
        apiKeyInput.type = type;
    });
    
    apiKeyInput.addEventListener('input', checkFormValidity);
}

// 检查表单有效性
function checkFormValidity() {
    const isValid = selectedFile && 
                   providerSelect.value && 
                   apiKeyInput.value.trim().length > 0;
    
    submitBtn.disabled = !isValid;
}

// 设置表单提交
function setupFormSubmit() {
    uploadForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        if (!selectedFile) return;
        
        // 显示加载状态
        const btnText = submitBtn.querySelector('.btn-text');
        const btnLoading = submitBtn.querySelector('.btn-loading');
        btnText.style.display = 'none';
        btnLoading.style.display = 'flex';
        submitBtn.disabled = true;
        
        try {
            // 1. 上传文件
            const formData = new FormData();
            formData.append('file', selectedFile);
            
            const uploadResponse = await fetch('/api/upload', {
                method: 'POST',
                body: formData
            });
            
            if (!uploadResponse.ok) {
                const error = await uploadResponse.json();
                throw new Error(error.detail || '上传失败');
            }
            
            const uploadResult = await uploadResponse.json();
            uploadedFileId = uploadResult.file_id;
            
            // 2. 启动翻译
            const translateResponse = await fetch('/api/translate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    file_id: uploadedFileId,
                    provider: providerSelect.value,
                    api_key: apiKeyInput.value,
                    model: modelSelect.value
                })
            });
            
            if (!translateResponse.ok) {
                const error = await translateResponse.json();
                throw new Error(error.detail || '启动翻译失败');
            }
            
            const translateResult = await translateResponse.json();
            
            // 3. 跳转到翻译进度页面
            window.location.href = `/translate/${translateResult.task_id}`;
            
        } catch (error) {
            alert('错误: ' + error.message);
            btnText.style.display = 'block';
            btnLoading.style.display = 'none';
            submitBtn.disabled = false;
            checkFormValidity();
        }
    });
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', init);
