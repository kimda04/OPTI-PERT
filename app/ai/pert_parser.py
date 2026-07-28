import re


class PertParser:

    @staticmethod
    def parse_ocr_text(text):

        lines = [
            line.strip()
            for line in text.split("\n")
            if line.strip()
        ]

        activities = []

        i = 0

        while i < len(lines):

            line = lines[i]

            if (
                len(line) == 1
                and line.isalpha()
            ):

                activity_id = line

                if i + 2 < len(lines):

                    name = lines[i + 1]

                    duration = lines[i + 2]


                    if duration.isdigit():

                        predecessors = []


                        if i + 3 < len(lines):

                            possible_pred = lines[i + 3]

                            if (
                                possible_pred != "-"
                                and len(possible_pred) == 1
                            ):
                                predecessors.append(
                                    possible_pred
                                )


                        activities.append(
                            {
                                "id": activity_id,
                                "name": name,
                                "duration": int(duration),
                                "predecessors": predecessors
                            }
                        )

                        i += 4
                        continue


            i += 1


        return activities