import os
import pytest
from playwright.sync_api import Page, expect

# Ensure screenshots directory exists
SCREENSHOT_DIR = "build/test-results/screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

def take_screenshot(page: Page, name: str):
    path = os.path.join(SCREENSHOT_DIR, f"{name}.png")
    page.screenshot(path=path, full_page=True)
    print(f"Screenshot saved to {path}")

def test_chat_flow(page: Page):
    # 1. Initial Load
    try:
        page.goto("http://localhost:8000", timeout=5000)
    except Exception:
        pytest.skip("Server not reachable at http://localhost:8000")

    take_screenshot(page, "01_initial_load")
    expect(page.locator(".header-title")).to_contain_text("AI Assistant")

    # 2. Typing a message
    chat_input = page.get_by_placeholder("Ask me anything...")
    chat_input.fill("Hello! Can you help me with a coding task?")
    take_screenshot(page, "02_message_typed")

    # 3. Sending the message
    # Intercept API request to verify/add headers if needed,
    # but the frontend should already send it.
    chat_input.press("Enter")
    take_screenshot(page, "03_message_sent")

    # 4. Wait for and verify response
    # In the updated CSS-based UI, we use .markdown-content
    assistant_msg = page.locator(".markdown-content").first
    expect(assistant_msg).to_be_visible(timeout=10000)
    take_screenshot(page, "04_response_received")

    # 5. Check response content
    content = assistant_msg.inner_text()
    assert len(content) > 0
    print(f"Assistant said: {content}")
