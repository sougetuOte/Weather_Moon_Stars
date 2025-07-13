import wx

# クリップボードにテキストをコピーする
def copy_to_clipboard(text):
    if wx.TheClipboard.Open():
        wx.TheClipboard.SetData(wx.TextDataObject(text))
        wx.TheClipboard.Close()
