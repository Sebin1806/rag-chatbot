import re


class ChunkService:

    @staticmethod
    def chunk_text(
        text: str,
        max_chunk_size: int = 800,
        overlap: int = 100
    ):

        if not text or not text.strip():
            return []

        # ----------------------------------------
        # Clean text
        # ----------------------------------------
        text = text.replace("\r\n", "\n")
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n{2,}", "\n", text)

        # ----------------------------------------
        # Split into lines
        # ----------------------------------------
        lines = [
            line.strip()
            for line in text.split("\n")
            if line.strip()
        ]

        chunks = []
        current_chunk = ""

        for line in lines:

            # ----------------------------------------
            # Detect section headings
            # ----------------------------------------
            is_heading = (
                line.isupper()
                or line.endswith(":")
                or (
                    len(line.split()) <= 5
                    and not line.startswith("•")
                    and len(line) < 60
                )
            )

            # ----------------------------------------
            # Start new chunk when heading appears
            # ----------------------------------------
            if is_heading and current_chunk:

                chunks.append(current_chunk.strip())
                current_chunk = line + "\n"
                continue

            # ----------------------------------------
            # Add line if it fits
            # ----------------------------------------
            if len(current_chunk) + len(line) + 1 <= max_chunk_size:

                current_chunk += line + "\n"

            else:

                chunks.append(current_chunk.strip())

                # Keep small overlap
                overlap_text = current_chunk[-overlap:]

                current_chunk = overlap_text + "\n" + line + "\n"

        # ----------------------------------------
        # Add final chunk
        # ----------------------------------------
        if current_chunk.strip():

            chunks.append(current_chunk.strip())

        # ----------------------------------------
        # Debug (temporary)
        # ----------------------------------------
        print("\n========== GENERATED CHUNKS ==========\n")

        for i, chunk in enumerate(chunks):

            print(f"\n----- Chunk {i} -----")
            print(chunk[:400])

        print("\n======================================\n")

        return chunks