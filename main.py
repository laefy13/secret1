import random
import requests
import string
import concurrent.futures
from filetracker import SegmentTrackerSQL
import argparse


class FoundSaveableSegment(Exception):
    pass


def generate_random_segment(length):
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(length))


def check_combinations(
    base_url,
    length,
    num_combinations,
    db_path,
    batch_size=1000,
    max_workers=20,
):
    tracker = SegmentTrackerSQL(db_path)

    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []
            segment_to_future = {}
            for _ in range(num_combinations):
                test_segment = generate_random_segment(length)

                if tracker.is_segment_tested(test_segment):
                    continue

                future = executor.submit(check_saveable, base_url, test_segment)
                futures.append(future)
                segment_to_future[future] = test_segment

                if len(futures) >= batch_size:
                    process_futures(futures, segment_to_future, tracker)
                    futures = []
                    segment_to_future = {}

            if futures:
                process_futures(futures, segment_to_future, tracker)
    except FoundSaveableSegment:
        print("Found one! Exiting...")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        tracker.close()


def process_futures(futures, segment_to_future, tracker):
    for future in concurrent.futures.as_completed(futures):
        test_segment = segment_to_future[future]
        result = future.result()
        if result is not None:
            status = result
            if status == "Saveable":
                print(f"Segment: {test_segment}")
                raise FoundSaveableSegment()
            tracker.add_segment(test_segment, status)


def check_saveable(base_url, test_segment):
    url = base_url + test_segment + ".m3u8?variant_version=1&tag=12"
    try:
        response = requests.get(url)
        result = "Saveable" if response.ok else "Not Saveable"
        return result
    except requests.exceptions.RequestException:
        return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", type=int, help="Post ID")
    parser.add_argument("--url", type=str, help="Will overwrite the URL + Post ID")
    parser.add_argument(
        "--db", type=str, default="/app/tested_segments.db", help="db path"
    )

    args = parser.parse_args()
    url = args.url
    id = args.id
    db_path = args.path

    if url:
        url = url
    elif id:
        url = f"https://video.twimg.com/ext_tw_video/{id}/pu/pl/"
    else:
        raise Exception("URL or ID not provided")

    check_combinations(
        url,
        16,
        100000,
        db_path=db_path,
        batch_size=1000,
        max_workers=20,
    )
