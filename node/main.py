if __name__ == '__main__':
    from utils.loggers.ilogger import logging
    logging('Starting application..', 'i')

    from protocols.startup import routine_001
    routine_001()  # engaging startup routine

    from uix.app import ChattingApp

    ChattingApp().run()
