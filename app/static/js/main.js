// 梨园书屋 - 主JavaScript文件

document.addEventListener('DOMContentLoaded', function() {
    initFlashMessages();
    initQuantityControls();
});

// 闪光消息自动消失
function initFlashMessages() {
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(msg => {
        setTimeout(() => {
            msg.style.animation = 'slideOut 0.3s ease forwards';
            setTimeout(() => msg.remove(), 300);
        }, 3000);
    });
}

// 数量选择器控制
function initQuantityControls() {
    document.querySelectorAll('.quantity-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const input = this.parentElement.querySelector('.quantity-input');
            const currentValue = parseInt(input.value) || 0;
            const min = parseInt(input.min) || 1;
            const max = parseInt(input.max) || 999;

            if (this.classList.contains('minus')) {
                input.value = Math.max(min, currentValue - 1);
            } else if (this.classList.contains('plus')) {
                input.value = Math.min(max, currentValue + 1);
            }
        });
    });
}

// 显示提示消息
function showToast(message, type = 'info') {
    const container = document.querySelector('.flash-messages') || createFlashContainer();

    const toast = document.createElement('div');
    toast.className = `flash-message flash-${type}`;
    toast.textContent = message;

    container.appendChild(toast);

    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease forwards';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

function createFlashContainer() {
    const container = document.createElement('div');
    container.className = 'flash-messages';
    document.body.appendChild(container);
    return container;
}

// 确认对话框
function confirmAction(message) {
    return confirm(message);
}

// 添加滑出动画
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOut {
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
