import re


class PertParser:


    @staticmethod
    def parse_speech_text(text):

        activities = []

        lines = text.split("\n")

        for line in lines:

            line = line.strip()

            if not line:
                continue

            match = re.search(
                r"([A-Za-z])\s.*?(\d+)",
                line
            )

            if match:

                name = match.group(1)

                duration = float(
                    match.group(2)
                )

                predecessor = []

                dependency = re.search(
                    r"depende de ([A-Za-z])",
                    line,
                    re.IGNORECASE
                )

                if dependency:
                    predecessor.append(
                        dependency.group(1)
                    )

                activities.append(
                    {
                        "name": name,
                        "description": "Importada por voz",
                        "optimistic": duration,
                        "most_likely": duration,
                        "pessimistic": duration,
                        "predecessors": predecessor
                    }
                )

        return activities



    @staticmethod
    def parse_ocr_text(text):

        activities = []

        lines = text.split("\n")


        for line in lines:

            line = line.strip()


            if not line:
                continue


            # Ignorar encabezados de tabla
            if (
                "ID" in line.upper()
                or "ACTIVIDAD" in line.upper()
                or "DURACIÓN" in line.upper()
            ):
                continue


            # Buscar filas tipo:
            # A Actividad A 3 -
            # B Diseño sistema 5 A

            match = re.search(
                r"([A-Za-z])\s+(.+?)\s+(\d+)\s*([A-Za-z,-]*)$",
                line
            )


            if match:


                name = match.group(1)

                description = match.group(2).strip()

                duration = float(
                    match.group(3)
                )


                predecessors_text = match.group(4)


                predecessors=[]


                if predecessors_text:

                    predecessors=[
                        p.strip()
                        for p in predecessors_text.split(",")
                    ]


                activities.append(
                    {
                        "name": name,

                        "description": description,

                        "duration": duration,

                        "optimistic": duration,

                        "most_likely": duration,

                        "pessimistic": duration,

                        "predecessors": predecessors
                    }
                )


        return activities