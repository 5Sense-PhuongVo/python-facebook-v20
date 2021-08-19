"""
    Tests for user api.
"""

import responses


def test_get_info(helpers, api):
    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{api.version}/{api.instagram_business_id}",
            json=helpers.load_json("testdata/instagram/apidata/users/user_fields.json"),
        )

        user = api.user.get_info()
        assert user.id == api.instagram_business_id

        user_json = api.user.get_info(
            fields="id,biography,name,username,profile_picture_url,followers_count,media_count",
            return_json=True,
        )
        assert user_json["id"] == api.instagram_business_id


def test_discovery_user(helpers, api):
    username = "facebookfordevelopers"

    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{api.version}/{api.instagram_business_id}",
            json=helpers.load_json(
                "testdata/instagram/apidata/discovery/medias_p1.json"
            ),
        )

        user = api.user.discovery_user(username=username)
        assert user.business_discovery.id == "17841407673135339"

        user_json = api.user.discovery_user(
            username=username,
            return_json=True,
        )
        assert user_json["business_discovery"]["id"] == "17841407673135339"


def test_discovery_media(helpers, api):
    username = "facebookfordevelopers"

    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{api.version}/{api.instagram_business_id}",
            json=helpers.load_json(
                "testdata/instagram/apidata/discovery/medias_p1.json"
            ),
        )
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{api.version}/{api.instagram_business_id}",
            json=helpers.load_json(
                "testdata/instagram/apidata/discovery/medias_p2.json"
            ),
        )

        media_p1 = api.user.discovery_user_medias(username=username, limit=2)
        media_p2 = api.user.discovery_user_medias(
            username=username,
            limit=2,
            after=media_p1.business_discovery.media.paging.cursors.after,
        )
        assert len(media_p1.business_discovery.media.data) == 2
        assert len(media_p2.business_discovery.media.data) == 2

    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{api.version}/{api.instagram_business_id}",
            json=helpers.load_json(
                "testdata/instagram/apidata/discovery/medias_p2.json"
            ),
        )

        media = api.user.discovery_user_medias(
            username=username, limit=2, before="before", return_json=True
        )
        assert len(media["business_discovery"]["media"]["data"]) == 2


def test_get_content_publishing_limit(helpers, api):
    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{api.version}/{api.instagram_business_id}/content_publishing_limit",
            json=helpers.load_json(
                "testdata/instagram/apidata/users/content_publish_limit.json"
            ),
        )

        limit = api.user.get_content_publishing_limit()
        assert limit.data[0].config.quota_total == 25

        limit_json = api.user.get_content_publishing_limit(return_json=True)
        assert limit_json["data"][0]["quota_usage"] == 0
