from discord import SyncWebhook
from python_imagesearch.imagesearch import imagesearch

import argparse
import sys
import time


def is_login_screen():
    pos = imagesearch('./login-screen.png')
    return pos[0] != -1


def is_character_selection_screen():
    pos = imagesearch('./character-selection-screen-wotelko.png')
    if pos[0] != -1:
        return True

    pos = imagesearch('./character-selection-screen-classic.png')
    return pos[0] != -1


def send_dummy_notification(message):
    print(message)


def send_discord_notification(message):
    print(message)

    webhook = SyncWebhook.from_url('https://discord.com/api/webhooks/1026520108882993182/xv2wxOqGJ7qpu7OifdCn5m8sGBiJ-HlnCk-pSnzSuujiK1EcgQ1sk_NPLdOC9qOrNCPO')
    webhook.send(message)


def main():
    if args.dummy_notification:
        notification_function = send_dummy_notification
    elif args.discord_notification:
        notification_function = send_discord_notification

    print(f'Starting watching for main login screen with notification function: {notification_function.__name__} with '
          f'interval {args.interval}s...')
    print(f'Please remember that WoW client window must be visible at all times!')

    while True:
        if args.notify_on_login_screen and is_login_screen():
            notification_function('Login screen detected!')
        elif args.notify_on_character_selection_screen and is_character_selection_screen():
            notification_function('Character selection screen detected!')
        else:
            print('Login nor character selection screen detected (which is assumed to be fine...)')

        time.sleep(args.interval)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='After you launch the script make sure to have WoW client fully visible on your main screen.'
    )

    parser.add_argument('--notify-on-login-screen',
                        help='notification trigger - send notification when login screen is detected',
                        action=argparse.BooleanOptionalAction)
    parser.add_argument('--notify-on-character-selection-screen',
                        help='notification trigger - send notification when character selection screen is detected',
                        action=argparse.BooleanOptionalAction)

    parser.add_argument('--dummy-notification',
                        help='notification type - dummy notification type used for testing',
                        action=argparse.BooleanOptionalAction)
    parser.add_argument('--discord-notification',
                        help='notification type - sends a notification to Discord channel and server specified by the '
                             'webhook (https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks)',
                        action=argparse.BooleanOptionalAction)

    parser.add_argument('--discord-webhook',
                        help='Address of your server\'s webhook')

    parser.add_argument('--interval', type=int, default=15, required=False)
    args = parser.parse_args()

    if not args.notify_on_login_screen and not args.notify_on_character_selection_screen:
        print('You need to select at least one type notification trigger')
        sys.exit(1)

    if not args.dummy_notification and not args.discord_notification:
        print('You need to select a notification type')
        sys.exit(1)

    if args.discord_notification and not args.discord_webhook:
        print('You need to provide Discord webhook address '
              '(https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks) in order to send Discord '
              'notification')
        sys.exit(1)

    main()
