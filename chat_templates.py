import os
css = '''
<style>
[data-testid="stAppViewContainer"] {
background-color: #1c4966;
}
.caht-message {
  padding: 1.5rem;
  border: 1px solid #fdfdfd;
  border-radius: 5px;
  margin-bottom: 10px;
  display: flex
}

.chat-message.user {
  background-color: #fdfdfd;
}

.chat-message.bot {
  background-color: #d6cfcf;
}

.chat-message .avatar {
  width: 15%;
}

.chat-message .avatar img {
  max-width: 78px;
  max-height: 78px;
  border-radius: 50%;
  object-fit: cover;
}

.chat-message .message {
  width: 85%;
  padding: 0 1.5rem;
  color: #000;
}

[class="css-10trblm e1nzilvr0"], [class="css-16idsys e1nzilvr4"]{
color: #fff
}

.chat-message.user.dark-mode {
  background-color: #2b313e;
}

.chat-message.bot.dark-mode {
  background-color: #475063
}
</style>
'''

logo_path = os.path.join(os.getcwd(), "logo.png")
bot_template = f'''
<div class="chat-message bot">
    <div class="avatar">
        <img src="{logo_path}" alt="error">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = f'''
<div class="chat-message user">
    <div class="avatar">
        <img src="{logo_path}" alt="error">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''
