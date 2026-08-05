# Copyright (c) 2025 AnonymousX1025
# Licensed under the MIT License.
# This file is part of AnonXMusic


import os
import re
import yt_dlp
import random
import asyncio
import aiohttp
from pathlib import Path

from py_yt import Playlist, VideosSearch

from anony import logger
from anony.helpers import Track, utils

# API Configuration
API_URL = os.environ.get("SHRUTI_API_URL", "https://api.shrutibots.site")
API_KEY = os.environ.get("SHRUTI_API_KEY", "ShrutiBotsV311lfYbnrxJ86SGBQ3U")

# Corrected Netscape Cookie Format (Separated by Tab \t)
EMBEDDED_COOKIES = (
    ".youtube.com\tTRUE\t/\tTRUE\t1788834227\tVISITOR_PRIVACY_METADATA\tCgJNTRIEGgAgZg%3D%3D\n"
    ".youtube.com\tTRUE\t/\tTRUE\t1807842226\t__Secure-3PSID\tg.a0007gjBkEY2gKuIK-IDNA4O9IE8wiocn8xv3WOp-JbD6KKxZwXounGOWJraQeCKpqG-oSwq9wACgYKAZkSARISFQHGX2MizRsEjWIBfOf8FT3Y3LMa_RoVAUF8yKpOPp3cWUdYQ5Ao5O96IuJM0076\n"
    ".youtube.com\tTRUE\t/\tTRUE\t1773283987\tGPS\t1\n"
    ".youtube.com\tTRUE\t/\tFALSE\t1804818233\tSIDCC\tAKEyXzW1sqaKu6ScKuu9DKvRXkDOUkGb35L6HhIlYENKXlnQKqsd44MpPeDXCEVNXNiXMxq4\n"
    ".youtube.com\tTRUE\t/\tTRUE\t1773368661\tYSC\tV5xhbUOi2aM\n"
    ".youtube.com\tTRUE\t/\tFALSE\t1807842226\tSID\tg.a0007gjBkEY2gKuIK-IDNA4O9IE8wiocn8xv3WOp-JbD6KKxZwXoYEH2e75zTffKW0Xjy7JjNAACgYKAYYSARISFQHGX2Miw6hqbohoy53Wf7whYiki9xoVAUF8yKqy6CRK8cS9icqdLlHz7eND0076\n"
    ".youtube.com\tTRUE\t/\tTRUE\t1804818226\t__Secure-1PSIDTS\tsidts-CjUBBj1CYnb_2un-x8U3DosdFcqPYVJhbg8Bk68ZCnIivIxZ-HGzJjNZhZ3mKsTTKPb9rfqcrxAA\n"
    ".youtube.com\tTRUE\t/\tTRUE\t1773282831\tCONSISTENCY\tAG2Tqf8zG-huG-xjZAla2JPHKiMEKIrXDCYwlOHHGuhn4BqYzEQeeWHU4KBqrAnF4gXzuExsDwlRUzVRXKDOoYbqs5Cc2zhXioJl1PDof9f5T3qYUl27a9fnzomuUSXtDrxnp1hPZjCN1LI5o2cd_BCb\n"
    ".youtube.com\tTRUE\t/\tTRUE\t1807842226\tSAPISID\tool8aM3EyPScJD-Y/A2ZqSKUfmKB11OwXW\n"
    ".youtube.com\tTRUE\t/\tTRUE\t1804818233\t__Secure-1PSIDCC\tAKEyXzWE3s3Z4jjWsZL2ADVxRV8QrrovXNLf3fLjfD9yjEGzPH3nS1nBe6mDRNa_Z19OZUfKZw\n"
    ".youtube.com\tTRUE\t/\tTRUE\t1807842226\tSSID\tAT0hp-hXDaolbHwv7\n"
    ".youtube.com\tTRUE\t/\tTRUE\t1807842226\t__Secure-1PAPISID\tool8aM3EyPScJD-Y/A2ZqSKUfmKB11OwXW\n"
    ".youtube.com\tTRUE\t/\tTRUE\t1807842226\t__Secure-1PSID\tg.a0007gjBkEY2gKuIK-IDNA4O9IE8wiocn8xv3WOp-JbD6KKxZwXo1xo64CJRyhnVfADBa2PqOgACgYKAV0SARISFQHGX2Mi1ad7QdhlGEysEgNracH2bhoVAUF8yKreHDECH5KvXV8UNvE31fIb0076\n"
    ".youtube.com\tTRUE\t/\tTRUE\t1807842226\t__Secure-3PAPISID\tool8aM3EyPScJD-Y/A2ZqSKUfmKB11OwXW\n"
    ".youtube.com\tTRUE\t/\tTRUE\t1804818233\t__Secure-3PSIDCC\tAKEyXzUDsCV5ZzeaZ8_RRuemevoTvbJutsmPMlGkA6CmKMPY1zz4f5-mKS5HuYiYODFDpNNRRg\n"
    ".youtube.com\tTRUE\t/\tTRUE\t1804818226\t__Secure-3PSIDTS\tsidts-CjUBBj1CYnb_2un-x8U3DosdFcqPYVJhbg8Bk68ZCnIivIxZ-HGzJjNZhZ3mKsTTKPb9rfqcrxAA\n"
    ".youtube.com\tTRUE\t/\tTRUE\t1788834187\tSecure-YNID\t16.YT=GlwsbGn0fwwI-d-fno4xNR8ODUrXPmpXzVPd0Yw-YqCAZRTG2HLiCB6OPx_wu7cH-QOOa2ymy52RM-yS5A3yX2uA8Dp09uFhXKuV7krGSttP2UxmiC8yLsmvqa3Koezzs8cgbS5HZA8hQw6hVBJNPumr8rBZqjn0ehTKVK53mbtKU3iIf96Cquwc-hHR71SIqwN0TiSUPz3iQcwSl59oahyvxBQJrswqogCv1UEvAKwHWO9pQVvPhI7yj19BukJzfaYdJpxM8eI0Ixp97WheNpkhT5n_qZm6xu_Go9dmMGTglnchyztzIzxRy0iS7SBky383yf7gUUuQTjcFvwCQ\n"
    ".youtube.com\tTRUE\t/\tFALSE\t1807842226\tAPISID\tr2h8dJdwnPtOnB6w/A696rI3lpsRhDG7gE\n"
    ".youtube.com\tTRUE\t/\tFALSE\t1807842226\tHSID\tAKFaV2VhVw1F0A1Ki\n"
    ".youtube.com\tTRUE\t/\tTRUE\t1807842227\tLOGIN_INFO\tAFmmF2swRAIgcB7wcOs4WNVu-ntf7mqpZ0eDodNht4tOYj9GjX_22kcCIDZ6go5sU7AJYiXaiXvDo7RTNDux2DRqDwi5aMYf_6dA:QUQ3MjNmd2RNVmZwS2M4ajJCX0NDQTZRLUhZUERGOVU3ekR3UWpkZVZ3QXVwZ1JEWmM5cDExQWV4MzRzaXF5bS1uY0dFTUlDcDJySkVkd3pZbFRVc29uSEtKT0tscDRDOG93c3Zxd0R1ZkZCTlBYcGdqaFVzMWhhOTZaRWlwTDF6WDJWU0tiM3FmRW05dUlkMlVndFROblhyejBxeGc2a09R\n"
    ".youtube.com\tTRUE\t/\tTRUE\t1807842230\tPREF\ttz=Asia.Rangoon&f7=100&f4=4000000\n"
    ".youtube.com\tTRUE\t/\tTRUE\t1788834227\tVISITOR_INFO1_LIVE\trQRaTxG5Dg8\n"
)


class YouTube:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        self.cookies = []
        self.checked = False
        self.cookie_dir = "anony/cookies"
        self.warned = False
        self.regex = re.compile(
            r"(https?://)?(www\.|m\.|music\.)?"
            r"(youtube\.com/(watch\?v=|shorts/|playlist\?list=)|youtu\.be/)"
            r"([A-Za-z0-9_-]{11}|PL[A-Za-z0-9_-]+)([&?][^\s]*)?"
        )
        self.iregex = re.compile(
            r"https?://(?:www\.|m\.|music\.)?(?:youtube\.com|youtu\.be)"
            r"(?!/(watch\?v=[A-Za-z0-9_-]{11}|shorts/[A-Za-z0-9_-]{11}"
            r"|playlist\?list=PL[A-Za-z0-9_-]+|[A-Za-z0-9_-]{11}))\S*"
        )

        self._ensure_embedded_cookies()

    def _ensure_embedded_cookies(self):
        """အကယ်၍ cookie ဖိုင်မရှိပါက (သို့) Format မှားနေပါက auto ရေးသွင်းမည်"""
        try:
            os.makedirs(self.cookie_dir, exist_ok=True)
            default_cookie_file = os.path.join(self.cookie_dir, "youtube.txt")

            # အသစ်ပြန်လည်ရေးသားမည်
            with open(default_cookie_file, "w", encoding="utf-8") as f:
                f.write(EMBEDDED_COOKIES)
            logger.info("Embedded YouTube cookies saved successfully.")
        except Exception as e:
            logger.error(f"Failed to write embedded cookies: {e}")

    def get_cookies(self):
        if not self.checked:
            if os.path.exists(self.cookie_dir):
                for file in os.listdir(self.cookie_dir):
                    if file.endswith(".txt"):
                        self.cookies.append(f"{self.cookie_dir}/{file}")
            self.checked = True
        if not self.cookies:
            if not self.warned:
                self.warned = True
                logger.warning("Cookies are missing; downloads might fail.")
            return None
        return random.choice(self.cookies)

    async def save_cookies(self, urls: list[str]) -> None:
        logger.info("Saving cookies from urls...")
        os.makedirs(self.cookie_dir, exist_ok=True)
        async with aiohttp.ClientSession() as session:
            for url in urls:
                name = url.split("/")[-1]
                link = "https://batbin.me/raw/" + name
                async with session.get(link) as resp:
                    resp.raise_for_status()
                    with open(f"{self.cookie_dir}/{name}.txt", "wb") as fw:
                        fw.write(await resp.read())
        logger.info(f"Cookies saved in {self.cookie_dir}.")

    def valid(self, url: str) -> bool:
        return bool(re.match(self.regex, url))

    def invalid(self, url: str) -> bool:
        return bool(re.match(self.iregex, url))

    async def search(self, query: str, m_id: int, video: bool = False) -> Track | None:
        try:
            _search = VideosSearch(query, limit=1, with_live=False)
            results = await _search.next()
        except Exception:
            return None
        if results and results["result"]:
            data = results["result"][0]
            return Track(
                id=data.get("id"),
                channel_name=data.get("channel", {}).get("name"),
                duration=data.get("duration"),
                duration_sec=utils.to_seconds(data.get("duration")),
                message_id=m_id,
                title=data.get("title")[:25],
                thumbnail=data.get("thumbnails", [{}])[-1].get("url").split("?")[0],
                url=data.get("link"),
                view_count=data.get("viewCount", {}).get("short"),
                video=video,
            )
        return None

    async def playlist(self, limit: int, user: str, url: str, video: bool) -> list[Track | None]:
        tracks = []
        try:
            plist = await Playlist.get(url)
            for data in plist["videos"][:limit]:
                track = Track(
                    id=data.get("id"),
                    channel_name=data.get("channel", {}).get("name", ""),
                    duration=data.get("duration"),
                    duration_sec=utils.to_seconds(data.get("duration")),
                    title=data.get("title")[:25],
                    thumbnail=data.get("thumbnails")[-1].get("url").split("?")[0],
                    url=data.get("link").split("&list=")[0],
                    user=user,
                    view_count="",
                    video=video,
                )
                tracks.append(track)
        except Exception:
            pass
        return tracks

    async def download(self, video_id: str, video: bool = False) -> str | None:
        url = self.base + video_id
        ext = "mp4" if video else "webm"
        filename = f"downloads/{video_id}.{ext}"

        if Path(filename).exists() and Path(filename).stat().st_size > 0:
            return filename

        os.makedirs("downloads", exist_ok=True)
        api_type = "video" if video else "audio"

        # --- 1. ပထမဦးဆုံး ShrutiBots API ဖြင့် Download ဆွဲရန် ကြိုးစားမည် ---
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{API_URL}/download",
                    params={"url": video_id, "type": api_type, "api_key": API_KEY},
                    timeout=aiohttp.ClientTimeout(total=300)
                ) as resp:
                    if resp.status == 200:
                        with open(filename, "wb") as f:
                            async for chunk in resp.content.iter_chunked(131072):
                                f.write(chunk)
                        if Path(filename).exists() and Path(filename).stat().st_size > 0:
                            return filename
        except Exception as e:
            logger.warning(f"ShrutiBots API failed, falling back to yt-dlp: {e}")

        # အကယ်၍ API ကျသွားလျှင် (သို့) Error တက်လျှင် ဖိုင်အကျိုးအပဲ့များကို ဖယ်ရှားမည်
        if Path(filename).exists():
            try:
                os.remove(filename)
            except Exception:
                pass

        # --- 2. API မအောင်မြင်ပါက yt_dlp ဖြင့် Cookies အသုံးပြု၍ Download ဆွဲမည် ---
        cookie = self.get_cookies()
        base_opts = {
            "outtmpl": "downloads/%(id)s.%(ext)s",
            "quiet": True,
            "noplaylist": True,
            "geo_bypass": True,
            "no_warnings": True,
            "overwrites": False,
            "nocheckcertificate": True,
            "cookiefile": cookie,
        }

        if video:
            ydl_opts = {
                **base_opts,
                "format": "(bestvideo[height<=?720][width<=?1280][ext=mp4])+(bestaudio)",
                "merge_output_format": "mp4",
            }
        else:
            ydl_opts = {
                **base_opts,
                "format": "bestaudio[ext=webm][acodec=opus]",
            }

        def _download():
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                try:
                    ydl.download([url])
                except (yt_dlp.utils.DownloadError, yt_dlp.utils.ExtractorError) as e:
                    logger.error(f"yt-dlp DownloadError: {e}")
                    return None
                except Exception as ex:
                    logger.warning("Download failed: %s", ex)
                    return None
            return filename

        result_file = await asyncio.to_thread(_download)
        if result_file and Path(result_file).exists() and Path(result_file).stat().st_size > 0:
            return result_file
        return None
