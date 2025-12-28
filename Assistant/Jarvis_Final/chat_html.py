class chat_html:
    top = """<style>
* {
  font-family: 'Lucida Sans Unicode';
  font-size: large;
}
.bubbleWrapper {
	padding: 20px;
  color: #fff;
}
.inlineContainerBot {
  margin-right: 100px;
}
.inlineContainerUser {
  margin-left: 100px;
}
.UserBubble {
	min-width: 60px;
	max-width: 700px;
	padding: 15px;
  margin: 6px 8px;
	background-color: #548BCC;
	border-radius: 16px 16px 0 16px;
	border: 1px solid #443f56;
 
}
.BotBubble {
	min-width: 60px;
	max-width: 700px;
	padding: 15px;
  margin: 6px 8px;
	background-color: #2C3F56;
	border-radius: 16px 16px 16px 0;
	border: 1px solid #54788e;
  
}
</style>
<div>
        <h2>Welcome to the crash team's very own ChatBot!!</h2>
"""
    html_contents = ""

    bot_text = """
<div class="bubbleWrapper" align="left">
                <div class="inlineContainerBot">
                        <div align="left">
                                <table>
                                <tr>
                                <td class="BotBubble">bot_text</td>
                                </tr>
                        </div>
                </div>
</div>
"""

    user_text = """
<div class="bubbleWrapper" align="right">
                <div class="inlineContainerUser">
                        <div align="right">
                               <table>
                                <tr>
                                <td class="UserBubble">user_text</td>
                                </tr>
                        </div>
                </div>
</div>
"""

    image_text = """
<br /><img src="image_path"/> '
"""

    bottom = """
</div>
"""

    html_text = top + html_contents + bottom

    def add_text(self, text_string, person):
        if person == 'bot':
            self.html_contents = self.html_contents + self.bot_text.replace('bot_text', text_string)
        else:
            self.html_contents = self.html_contents + self.user_text.replace('user_text', text_string)

        self.html_text = self.top + self.html_contents + self.bottom

    def add_image(self, image_path):
        self.html_contents = self.html_contents + self.image_text.replace('image_path', image_path)
        self.html_text = self.top + self.html_contents + self.bottom
