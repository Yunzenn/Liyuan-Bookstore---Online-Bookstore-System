// 网上书店 - 主JavaScript文件

document.addEventListener('DOMContentLoaded', function() {
    // 初始化闪光消息自动消失
    initFlashMessages();

    // 初始化导航栏滚动效果
    initNavbarScroll();

    // 初始化卡片鼠标跟踪效果
    initCardHoverEffect();
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

// 导航栏滚动效果
function initNavbarScroll() {
    const navbar = document.querySelector('.navbar');
    if (!navbar) return;

    let lastScroll = 0;
    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;

        if (currentScroll > 100) {
            navbar.style.background = 'rgba(17, 17, 17, 0.95)';
            navbar.style.boxShadow = '0 8px 32px rgba(0, 0, 0, 0.3)';
        } else {
            navbar.style.background = 'rgba(17, 17, 17, 0.8)';
            navbar.style.boxShadow = 'none';
        }

        lastScroll = currentScroll;
    });
}

// 卡片鼠标跟踪发光效果
function initCardHoverEffect() {
    const cards = document.querySelectorAll('.book-card, .order-card, .card');

    cards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            card.style.setProperty('--mouse-x', `${x}px`);
            card.style.setProperty('--mouse-y', `${y}px`);

            // 添加动态光晕
            if (!card.querySelector('.card-glow')) {
                const glow = document.createElement('div');
                glow.className = 'card-glow';
                glow.style.cssText = `
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    pointer-events: none;
                    background: radial-gradient(300px circle at var(--mouse-x) var(--mouse-y),
                        rgba(59, 130, 246, 0.1),
                        transparent 50%);
                    border-radius: inherit;
                    opacity: 0;
                    transition: opacity 0.3s;
                `;
                card.style.position = 'relative';
                card.appendChild(glow);
            }

            const glow = card.querySelector('.card-glow');
            glow.style.opacity = '1';
        });

        card.addEventListener('mouseleave', () => {
            const glow = card.querySelector('.card-glow');
            if (glow) {
                glow.style.opacity = '0';
            }
        });
    });
}

// 显示加载状态
function showLoading(button) {
    const originalText = button.textContent;
    button.disabled = true;
    button.innerHTML = '<span class="loading"></span> 处理中...';
    return originalText;
}

// 隐藏加载状态
function hideLoading(button, originalText) {
    button.disabled = false;
    button.textContent = originalText;
}

// 确认对话框
function confirmAction(message) {
    return new Promise((resolve) => {
        const result = confirm(message);
        resolve(result);
    });
}

// 格式化价格
function formatPrice(price) {
    return `¥${parseFloat(price).toFixed(2)}`;
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
