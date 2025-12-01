
class Duration:
    """
    A helper utility class for converting and handling
    duration values in mm:ss format and seconds.
    """

    @staticmethod
    def to_seconds(time_str):
        """
        Convert a mm:ss string into total seconds.
        Example: "03:45" → 225
        """
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
        """
        Convert seconds → mm:ss formatted string.
        Example: 225 → "03:45"
        """
        if seconds < 0:
            seconds = 0

        mm = seconds // 60
        ss = seconds % 60
        return f"{mm:02d}:{ss:02d}"

    @staticmethod
    def add(time1, time2):
        """
        Add two mm:ss duration strings.
        Example: "01:20" + "02:30" = "03:50"
        """
        sec_total = Duration.to_seconds(time1) + Duration.to_seconds(time2)
        return Duration.to_mmss(sec_total)

    @staticmethod
    def sum(track_list):
        """
        Sum durations of track objects that have .duration (mm:ss).
        Example: [Track(), Track(), ...]
        Returns total seconds.
        """
        total = 0
        for t in track_list:
            total += Duration.to_seconds(t.duration)
        return total
