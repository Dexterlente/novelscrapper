from seleniumbase import SB

def solve_captcha(sb: SB):
    sb.uc_gui_click_captcha()
    sb.assert_element('img[alt="Light Novel Cave"]', timeout=3)
