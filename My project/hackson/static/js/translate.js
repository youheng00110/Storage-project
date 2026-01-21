/**
 * 翻译进度页面 JavaScript
 */

// DOM 元素
const statusIcon = document.getElementById('statusIcon');
const statusText = document.getElementById('statusText');
const statusMessage = document.getElementById('statusMessage');
const progressFill = document.getElementById('progressFill');
const progressText = document.getElementById('progressText');
const actionButtons = document.getElementById('actionButtons');
const downloadBtn = document.getElementById('downloadBtn');
const previewSection = document.getElementById('previewSection');
const previewContent = document.getElementById('previewContent');

// 状态轮询间隔
let pollInterval = null;
const POLL_INTERVAL_MS = 2000;

// 初始化
function init() {
    if (!taskId) {
        statusText.textContent = '错误';
        statusMessage.textContent = '任务 ID 无效';
        return;
    }
    
    // 开始轮询状态
    pollStatus();
    pollInterval = setInterval(pollStatus, POLL_INTERVAL_MS);
}

// 轮询翻译状态
async function pollStatus() {
    try {
        const response = await fetch(`/api/status/${taskId}`);
        
        if (!response.ok) {
            throw new Error('获取状态失败');
        }
        
        const data = await response.json();
        updateUI(data);
        
        // 如果完成或失败，停止轮询
        if (data.status === 'completed' || data.status === 'failed') {
            clearInterval(pollInterval);
        }
        
    } catch (error) {
        console.error('状态查询错误:', error);
    }
}

// 更新 UI
function updateUI(data) {
    // 更新进度条
    progressFill.style.width = `${data.progress}%`;
    progressText.textContent = `${data.progress}%`;
    
    // 更新状态信息
    statusMessage.textContent = data.message;
    
    switch (data.status) {
        case 'pending':
            statusText.textContent = '准备中...';
            break;
            
        case 'processing':
            statusText.textContent = '翻译中...';
            break;
            
        case 'completed':
            statusText.textContent = '翻译完成';
            showCompleted(data);
            break;
            
        case 'failed':
            statusText.textContent = '翻译失败';
            showFailed(data);
            break;
    }
}

// 显示完成状态
function showCompleted(data) {
    // 更新图标
    statusIcon.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2">
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
            <polyline points="22 4 12 14.01 9 11.01"/>
        </svg>
    `;
    statusIcon.classList.add('success');
    
    // 显示操作按钮
    actionButtons.style.display = 'flex';
    downloadBtn.href = `/api/download/${taskId}`;
    
    // 加载预览
    loadPreview();
}

// 显示失败状态
function showFailed(data) {
    // 更新图标
    statusIcon.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="#ef4444" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <line x1="15" y1="9" x2="9" y2="15"/>
            <line x1="9" y1="9" x2="15" y2="15"/>
        </svg>
    `;
    statusIcon.classList.add('error');
    
    // 只显示返回按钮
    actionButtons.style.display = 'flex';
    downloadBtn.style.display = 'none';
}

// 加载预览内容
async function loadPreview() {
    try {
        const response = await fetch(`/api/download/${taskId}`);
        
        if (response.ok) {
            const text = await response.text();
            previewContent.textContent = text.substring(0, 2000) + (text.length > 2000 ? '\n\n... (内容已截断，请下载完整文件)' : '');
            previewSection.style.display = 'block';
        }
    } catch (error) {
        console.error('加载预览失败:', error);
    }
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', init);
