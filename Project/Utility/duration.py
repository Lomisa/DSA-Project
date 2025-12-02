
class Duration:
    @staticmethod
    def to_seconds(time_str):
        try:
            parts = time_str.split(":")
            if len(parts) != 2:
                raise ValueError

            mm, ss = parts
            mm = int(mm)
            ss = int(ss)

            if mm < 0 or ss < 0 or ss >= 60:
                raise ValueError

            return mm * 60 + ss

        except:
            raise ValueError(f"Invalid duration format '{time_str}'. Expected mm:ss")

    @staticmethod
    def to_mmss(seconds):
        if seconds < 0:
            seconds = 0

        mm = seconds // 60
        ss = seconds % 60
        return f"{mm:02d}:{ss:02d}"

    @staticmethod
    def add(time1, time2):
        sec_total = Duration.to_seconds(time1) + Duration.to_seconds(time2)
        return Duration.to_mmss(sec_total)

    @staticmethod
    def sum(track_list):
        total = 0
        for t in track_list:
            total += Duration.to_seconds(t.duration)
        return total

