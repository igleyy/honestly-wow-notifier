from discord import SyncWebhook
from python_imagesearch.imagesearch import imagesearch

import argparse
import sys
import time


def is_login_screen():
    pos = imagesearch(f'./samples/login-screen-{args.resolution}.png')
    return pos[0] != -1


def is_character_selection_screen():
    pos = imagesearch(f'./samples/character-selection-screen-wotelko-{args.resolution}.png')
    if pos[0] != -1:
        return True

    pos = imagesearch(f'./samples/character-selection-screen-classic-{args.resolution}.png')
    return pos[0] != -1


def send_dummy_notification(message):
    print(message)


def send_discord_notification(message):
    print(message)

    webhook = SyncWebhook.from_url(args.discord_webhook)
    webhook.send(message)


def exit_and_wait_for_keypress():
    input("Press Enter to continue...")
    sys.exit(1)


def main():
    if args.dummy_notification:
        notification_function = send_dummy_notification
    elif args.discord_notification:
        notification_function = send_discord_notification

    print(f'Notification function: {notification_function.__name__}. Check interval: interval {args.interval}s. '
          f'Current resolution is {args.resolution}. Please remember that WoW client window must be visible at all '
          f'times!\n')

    if args.notify_on_login_screen:
        print('The script will watch for login screen.')

    if args.notify_on_character_selection_screen:
        print('The script will watch for character selection screen.')

    while True:
        if is_login_screen() or is_character_selection_screen():
            notification_function('You better go check your WoW client!')
        else:
            print('.')

        time.sleep(args.interval)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='After you launch the script make sure to have WoW client fully visible on your main screen. '
                    'In order for detection to work your WoW client must be in Windowed display mode and resolution '
                    'must be 2560x1440 or you provide samples using your own resolution in samples/ directory.'
    )

    parser.add_argument('-l',
                        '--notify-on-login-screen',
                        help='notification trigger - send notification when login screen is detected',
                        action=argparse.BooleanOptionalAction)
    parser.add_argument('-c',
                        '--notify-on-character-selection-screen',
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

    parser.add_argument('-r',
                        '--resolution',
                        help='Resolution of your WoW client window in following format e.g. 2560x1440',
                        default='2560x1440'
                        )

    parser.add_argument('--interval', type=int, default=15, required=False)
    args = parser.parse_args()

    if not args.notify_on_login_screen and not args.notify_on_character_selection_screen:
        print('You need to select at least one type notification trigger')
        exit_and_wait_for_keypress()

    if not args.dummy_notification and not args.discord_notification:
        print('You need to select a notification type')
        exit_and_wait_for_keypress()

    if args.discord_notification and not args.discord_webhook:
        print('You need to provide Discord webhook address '
              '(https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks) in order to send Discord '
              'notification')
        exit_and_wait_for_keypress()

    main()
