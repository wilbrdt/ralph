"""edX to xAPI conversion sets."""

# flake8: noqa

from .navigational import UIPageCloseToPageTerminated
from .server import ServerEventToPageViewed
from .video import (
    UILoadVideoToVideoInitialized,
    UIPauseVideoToVideoPaused,
    UIPlayVideoToVideoPlayed,
    UISeekVideoToVideoSeeked,
    UIStopVideoToVideoTerminated,
)
