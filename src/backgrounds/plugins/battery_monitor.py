import psutil
import time
import logging

logger = logging.getLogger(__name__)

class BatteryMonitor:
    """
    Background plugin to monitor battery levels and alert on low battery for safety.
    """

    def __init__(self, config=None):
        """
        Initialize the BatteryMonitor with optional config.
        :param config: Dictionary with thresholds, e.g., {'low_threshold': 20}
        """
        self.config = config or {}
        self.low_threshold = self.config.get('low_threshold', 20)  # Default 20%
        self.critical_threshold = self.config.get('critical_threshold', 10)  # Default 10%
        self.check_interval = self.config.get('check_interval', 60)  # Seconds, default 1 minute
        self.alert_callback = self.config.get('alert_callback', self.default_alert)

    def default_alert(self, message):
        """
        Default alert method: logs the message.
        """
        logger.warning(message)

    def monitor(self):
        """
        Main monitoring loop. Runs indefinitely, checking battery every interval.
        """
        while True:
            try:
                battery = psutil.sensors_battery()
                if battery is None:
                    logger.error("No battery sensor available.")
                    break

                percent = battery.percent
                plugged = battery.power_plugged

                if not plugged:
                    if percent <= self.critical_threshold:
                        self.alert_callback(f"Critical battery level: {percent}%! Plug in immediately.")
                    elif percent <= self.low_threshold:
                        self.alert_callback(f"Low battery: {percent}%. Consider plugging in.")

                time.sleep(self.check_interval)
            except Exception as e:
                logger.error(f"Error in battery monitoring: {e}")
                time.sleep(self.check_interval)

# Entry point for the plugin
def init_plugin(config=None):
    """
    Initialize and return the BatteryMonitor instance.
    """
    return BatteryMonitor(config)

# If run as script (for testing)
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    monitor = init_plugin()
    monitor.monitor()