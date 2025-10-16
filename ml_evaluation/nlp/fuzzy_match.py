import re
from difflib import SequenceMatcher

def character_similarity_ratio(self, text: str, subset: str, biggest_allowed_gap: int = 25) -> float:
    """Compute similarity ratio between a text and a subset with allowed fuzzy matching.

    Args:
        text: The original text.
        subset: The subset string to validate.
        biggest_allowed_gap: the biggest character offset between two exact sub-string

    Returns:
        bool: True if the subset is found within the text allowing for 5% character differences.

    """
    # Remove non-alphanumeric characters for comparison
    non_alphanum_pattern = re.compile(r"[^a-zA-Z0-9]")
    text_clean = non_alphanum_pattern.sub("", text.lower())
    subset_clean = non_alphanum_pattern.sub("", subset.lower())

    # Try to find the best matching segment in the text
    matcher = SequenceMatcher(
        isjunk=None,
        a=text_clean,
        b=subset_clean,
        autojunk=False,
    )
    match_blocks = matcher.get_matching_blocks()

    # Concatenate nearby matching blocks  
    concatenated_blocks = []
    curr_idx = 0
    while curr_idx < len(match_blocks):
        curr_block = match_blocks[curr_idx]
        concat_block = {"start": curr_block.a, "end": curr_block.a + curr_block.size}
        curr_idx += 1
        for end_idx in range(curr_idx, len(match_blocks)):
            next_block = match_blocks[end_idx]
            if next_block.size and next_block.a <= concat_block["end"] + biggest_allowed_gap:
                concat_block["end"] = next_block.a + next_block.size
                curr_idx = end_idx
        self.logger.debug("Concatenated [%d:%d]: %s", concat_block["start"], concat_block["end"], text_clean[concat_block["start"]:concat_block["end"]])
        concatenated_blocks.append(concat_block)

    # Find the longest contiguous match
    longest_match = max(block["end"] - block["start"] for block in concatenated_blocks), default=0)  
    
    return longest_match / len(subset_clean)
