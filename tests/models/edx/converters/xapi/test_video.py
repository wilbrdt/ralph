"""Tests for the video event xAPI converter"""

import json
from uuid import UUID, uuid5

import pytest
from hypothesis import provisional

from ralph.models.converter import convert_dict_event
from ralph.models.edx.converters.xapi.video import (
    UILoadVideoToVideoInitialized,
    UIPauseVideoToVideoPaused,
    UIPlayVideoToVideoPlayed,
    UISeekVideoToVideoSeeked,
    UIStopVideoToVideoTerminated,
)
from ralph.models.edx.video.statements import (
    UILoadVideo,
    UIPauseVideo,
    UIPlayVideo,
    UISeekVideo,
    UIStopVideo,
)

from tests.fixtures.hypothesis_strategies import custom_given


@custom_given(UILoadVideo, provisional.urls())
@pytest.mark.parametrize("uuid_namespace", ["ee241f8b-174f-5bdb-bae9-c09de5fe017f"])
def test_ui_load_video_to_video_initialized(uuid_namespace, event, platform_url):
    """Tests that converting with `UILoadVideoToVideoInitialized` returns the
    expected xAPI statement.
    """

    event.context.course_id = ""
    event.context.org_id = ""
    event.context.user_id = "1"
    event_str = event.json()
    event = json.loads(event_str)
    xapi_event = convert_dict_event(
        event, event_str, UILoadVideoToVideoInitialized(uuid_namespace, platform_url)
    )
    xapi_event_dict = json.loads(xapi_event.json(exclude_none=True, by_alias=True))

    assert xapi_event_dict == {
        "id": str(uuid5(UUID(uuid_namespace), event_str)),
        "actor": {"account": {"homePage": platform_url, "name": "1"}},
        "verb": {
            "id": "http://adlnet.gov/expapi/verbs/initialized",
            "display": {"en-US": "initialized"},
        },
        "context": {
            "extensions": {
                "https://w3id.org/xapi/video/extensions/length": 0.0,
                "https://w3id.org/xapi/video/extensions/session-id": str(
                    UUID(event["session"])
                ),
                "https://w3id.org/xapi/video/extensions/user-agent": event["agent"],
            }
        },
        "object": {
            "id": platform_url
            + "/xblock/block-v1:"
            + event["context"]["course_id"]
            + "-course-v1:+type@video+block@"
            + event["event"]["id"],
            "definition": {
                "type": "https://w3id.org/xapi/video/activity-type/video",
                "name": {"en-US": event["event"]["id"]},
            },
        },
        "timestamp": event["time"],
        "version": "1.0.0",
    }


@custom_given(UIPlayVideo, provisional.urls())
@pytest.mark.parametrize("uuid_namespace", ["ee241f8b-174f-5bdb-bae9-c09de5fe017f"])
def test_ui_play_video_to_video_played(uuid_namespace, event, platform_url):
    """Tests that converting with `UIPlayVideoToVideoPlayed` returns the expected
    xAPI statement.
    """

    event.context.course_id = ""
    event.context.org_id = ""
    event.context.user_id = "1"
    event_str = event.json()
    event = json.loads(event_str)
    xapi_event = convert_dict_event(
        event, event_str, UIPlayVideoToVideoPlayed(uuid_namespace, platform_url)
    )
    xapi_event_dict = json.loads(xapi_event.json(exclude_none=True, by_alias=True))
    assert xapi_event_dict == {
        "id": str(uuid5(UUID(uuid_namespace), event_str)),
        "actor": {"account": {"homePage": platform_url, "name": "1"}},
        "verb": {
            "id": "https://w3id.org/xapi/video/verbs/played",
            "display": {"en-US": "played"},
        },
        "object": {
            "id": platform_url
            + "/xblock/block-v1:"
            + event["context"]["course_id"]
            + "-course-v1:+type@video+block@"
            + event["event"]["id"],
            "definition": {
                "type": "https://w3id.org/xapi/video/activity-type/video",
                "name": {"en-US": event["event"]["id"]},
            },
        },
        "result": {
            "extensions": {
                "https://w3id.org/xapi/video/extensions/time": event["event"][
                    "currentTime"
                ]
            }
        },
        "context": {
            "extensions": {
                "https://w3id.org/xapi/video/extensions/session-id": str(
                    UUID(event["session"])
                ),
            },
        },
        "timestamp": event["time"],
        "version": "1.0.0",
    }


@custom_given(UIPauseVideo, provisional.urls())
@pytest.mark.parametrize("uuid_namespace", ["ee241f8b-174f-5bdb-bae9-c09de5fe017f"])
def test_ui_pause_video_to_video_paused(uuid_namespace, event, platform_url):
    """Tests that converting with `UIPauseVideoToVideoPaused` returns the expected xAPI
    statement.
    """

    event.context.course_id = ""
    event.context.org_id = ""
    event.context.user_id = "1"
    event_str = event.json()
    event = json.loads(event_str)
    xapi_event = convert_dict_event(
        event, event_str, UIPauseVideoToVideoPaused(uuid_namespace, platform_url)
    )
    xapi_event_dict = json.loads(xapi_event.json(exclude_none=True, by_alias=True))
    assert xapi_event_dict == {
        "id": str(uuid5(UUID(uuid_namespace), event_str)),
        "actor": {"account": {"homePage": platform_url, "name": "1"}},
        "verb": {
            "id": "https://w3id.org/xapi/video/verbs/paused",
            "display": {"en-US": "paused"},
        },
        "object": {
            "id": platform_url
            + "/xblock/block-v1:"
            + event["context"]["course_id"]
            + "-course-v1:+type@video+block@"
            + event["event"]["id"],
            "definition": {
                "type": "https://w3id.org/xapi/video/activity-type/video",
                "name": {"en-US": event["event"]["id"]},
            },
        },
        "context": {
            "extensions": {
                "https://w3id.org/xapi/video/extensions/length": 0.0,
                "https://w3id.org/xapi/video/extensions/session-id": str(
                    UUID(event["session"])
                ),
            }
        },
        "result": {
            "extensions": {
                "https://w3id.org/xapi/video/extensions/time": event["event"][
                    "currentTime"
                ]
            }
        },
        "timestamp": event["time"],
        "version": "1.0.0",
    }


@custom_given(UIStopVideo, provisional.urls())
@pytest.mark.parametrize("uuid_namespace", ["ee241f8b-174f-5bdb-bae9-c09de5fe017f"])
def test_ui_stop_video_to_video_terminated(uuid_namespace, event, platform_url):
    """Tests that converting with `UIStopVideoToVideoTerminated` returns the expected
    xAPI statement.
    """

    event.context.course_id = ""
    event.context.org_id = ""
    event.context.user_id = "1"
    event_str = event.json()
    event = json.loads(event_str)
    xapi_event = convert_dict_event(
        event, event_str, UIStopVideoToVideoTerminated(uuid_namespace, platform_url)
    )
    xapi_event_dict = json.loads(xapi_event.json(exclude_none=True, by_alias=True))
    assert xapi_event_dict == {
        "id": str(uuid5(UUID(uuid_namespace), event_str)),
        "actor": {"account": {"homePage": platform_url, "name": "1"}},
        "verb": {
            "id": "http://adlnet.gov/expapi/verbs/terminated",
            "display": {"en-US": "terminated"},
        },
        "object": {
            "id": platform_url
            + "/xblock/block-v1:"
            + event["context"]["course_id"]
            + "-course-v1:+type@video+block@"
            + event["event"]["id"],
            "definition": {
                "type": "https://w3id.org/xapi/video/activity-type/video",
                "name": {"en-US": event["event"]["id"]},
            },
        },
        "context": {
            "extensions": {
                "https://w3id.org/xapi/video/extensions/length": 0.0,
                "https://w3id.org/xapi/video/extensions/session-id": str(
                    UUID(event["session"])
                ),
            }
        },
        "result": {
            "extensions": {
                "https://w3id.org/xapi/video/extensions/time": event["event"][
                    "currentTime"
                ],
                "https://w3id.org/xapi/video/extensions/progress": 0.0,
            }
        },
        "timestamp": event["time"],
        "version": "1.0.0",
    }


@custom_given(UISeekVideo, provisional.urls())
@pytest.mark.parametrize("uuid_namespace", ["ee241f8b-174f-5bdb-bae9-c09de5fe017f"])
def test_ui_seek_video_to_video_seeked(uuid_namespace, event, platform_url):
    """Tests that converting with `UISeekVideoToVideoSeeked` returns the expected
    xAPI statement.
    """

    event.context.course_id = ""
    event.context.org_id = ""
    event.context.user_id = "1"
    event_str = event.json()
    event = json.loads(event_str)
    xapi_event = convert_dict_event(
        event, event_str, UISeekVideoToVideoSeeked(uuid_namespace, platform_url)
    )
    xapi_event_dict = json.loads(xapi_event.json(exclude_none=True, by_alias=True))
    assert xapi_event_dict == {
        "id": str(uuid5(UUID(uuid_namespace), event_str)),
        "actor": {"account": {"homePage": platform_url, "name": "1"}},
        "verb": {
            "id": "https://w3id.org/xapi/video/verbs/seeked",
            "display": {"en-US": "seeked"},
        },
        "object": {
            "id": platform_url
            + "/xblock/block-v1:"
            + event["context"]["course_id"]
            + "-course-v1:+type@video+block@"
            + event["event"]["id"],
            "definition": {
                "type": "https://w3id.org/xapi/video/activity-type/video",
                "name": {"en-US": event["event"]["id"]},
            },
        },
        "result": {
            "extensions": {
                "https://w3id.org/xapi/video/extensions/time-from": event["event"][
                    "old_time"
                ],
                "https://w3id.org/xapi/video/extensions/time-to": event["event"][
                    "new_time"
                ],
            }
        },
        "context": {
            "extensions": {
                "https://w3id.org/xapi/video/extensions/session-id": str(
                    UUID(event["session"])
                ),
            },
        },
        "timestamp": event["time"],
        "version": "1.0.0",
    }
