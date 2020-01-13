from config import InstagramBot, argsParser

args = argsParser()
hashtag_list = ['sonyalpha', 'sonya7riii']
bot = InstagramBot(args.username, args.password, args.time)
bot.startBot(hashtag_list)
bot.closeBrowser()