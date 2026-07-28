import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

class WhitewallsBuster:
    def __init__(self, root):
        self.root = root
        self.root.title("白璧 8.0 破解器 🛡️")
        self.root.geometry("400x250")
        self.root.resizable(False, False)
        
        self.driver = None
        self.connected = False

        tk.Label(root, text="白璧 8.0 封屏破解工具", font=("微软雅黑", 16, "bold")).pack(pady=20)
        
        self.status_var = tk.StringVar()
        self.status_var.set("⏳ 未连接")
        tk.Label(root, textvariable=self.status_var, font=("微软雅黑", 10), fg="#555").pack()

        self.connect_btn = tk.Button(
            root, text="🔗 连接已打开的浏览器",
            command=self.connect_browser,
            bg="#4CAF50", fg="white", font=("微软雅黑", 12), width=20
        )
        self.connect_btn.pack(pady=10)

        self.bust_btn = tk.Button(
            root, text="💥 破解封屏",
            command=self.bust_whitewalls,
            bg="#FF5722", fg="white", font=("微软雅黑", 12), width=20,
            state=tk.DISABLED
        )
        self.bust_btn.pack(pady=10)

        tk.Label(root, text="提示：先连接浏览器，然后点击破解", font=("微软雅黑", 9), fg="#999").pack(pady=10)
    
    def connect_browser(self):
        """连接到已打开的 Chrome（调试模式）"""
        try:
            options = Options()
            options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
            self.driver = webdriver.Chrome(options=options)
            self.connected = True
            self.status_var.set("✅ 已连接到浏览器")
            self.bust_btn.config(state=tk.NORMAL)
            self.connect_btn.config(state=tk.DISABLED)
            messagebox.showinfo("成功", "已成功连接到浏览器！")
        except Exception as e:
            self.status_var.set(f"❌ 连接失败: {str(e)[:40]}...")
            messagebox.showerror("错误", f"连接失败！\n请确保 Chrome 已用调试模式启动。\n\n错误信息:\n{str(e)}")
    
    def bust_whitewalls(self):
        if not self.connected or self.driver is None:
            messagebox.showwarning("提示", "请先连接浏览器")
            return

        try:
            handles = self.driver.window_handles
            if handles:
                self.driver.switch_to.window(handles[-1])
        except:
            pass

        script = """
        (function() {
            console.log('🛡️ 启动破解...');

            // ===== 1. 删除封屏div =====
            const div = document.querySelector('div[style*="position: fixed"][style*="z-index: 99999"]');
            let deleted = false;
            if (div && div.textContent === 'White walls') {
                div.remove();
                deleted = true;
                console.log('✅ 白璧封屏已删除');
            }

            // ===== 2. 拦截跳转（优先使用 Navigation API，备选 beforeunload） =====
            try {
                // 尝试使用 Navigation API（无弹窗）
                if (window.navigation && typeof navigation.addEventListener === 'function') {
                    navigation.addEventListener('navigate', function(event) {
                        event.preventDefault();
                        console.log('🛡️ Navigation API 拦截跳转:', event.destination.url);
                    });
                    console.log('✅ Navigation API 已启用');
                } else {
                    // 降级方案：使用 beforeunload（会弹窗）
                    window.addEventListener('beforeunload', function(e) {
                        e.preventDefault();
                        e.returnValue = '';
                        console.log('🛡️ beforeunload 拦截跳转');
                    }, true);
                    console.log('⚠️ Navigation API 不支持，使用 beforeunload');
                }
            } catch(e) {
                console.warn('⚠️ 跳转拦截设置失败:', e);
                // 最坏情况：用轮询守卫
                const TARGET_URL = window.location.href;
                const guard = setInterval(function() {
                    if (window.location.href === 'about:blank' || window.location.href === '') {
                        console.warn('🚫 检测到跳转，强制返回...');
                        window.stop();
                        window.location.assign(TARGET_URL);
                    }
                }, 100);
                setTimeout(function() { clearInterval(guard); }, 10000);
            }

            // ===== 3. 清理白璧状态 =====
            try {
                const ext = Scratch?.extensions?._extensions?.['Whitewalls'];
                if (ext) {
                    if (ext._debuggerTimer) clearInterval(ext._debuggerTimer);
                    if (ext._detectTimer) clearInterval(ext._detectTimer);
                    if (ext._executionTimer) clearInterval(ext._executionTimer);
                    ext.isSealed = false;
                    ext.isBlocking = false;
                    if (ext._onKeyDown) window.removeEventListener('keydown', ext._onKeyDown);
                    if (ext._onContextMenu) document.removeEventListener('contextmenu', ext._onContextMenu);
                    console.log('✅ 白璧状态已清理');
                }
            } catch(e) {
                console.warn('⚠️ 清理白璧状态失败:', e);
            }

            console.log('✅ 破解完成！');
            return deleted;
        })();
    """

        try:
            result = self.driver.execute_script(script)
            if result:
                self.status_var.set("✅ 破解成功！页面功能正常")
                messagebox.showinfo("成功", "🎉 白璧已破解！\n页面功能已完全恢复。")
            else:
                self.status_var.set("ℹ️ 未检测到封屏")
        except Exception as e:
            self.status_var.set(f"❌ 失败: {str(e)[:40]}...")
            messagebox.showerror("错误", f"破解失败:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = WhitewallsBuster(root)
    root.mainloop()
