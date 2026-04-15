'use strict';

/**
 * Chunk text into ~500-word segments with ~50-word overlap.
 * Tries to split on paragraph boundaries.
 * @param {string} text
 * @param {number} [chunkWords=500]
 * @param {number} [overlapWords=50]
 * @returns {string[]}
 */
function chunkText(text, chunkWords = 500, overlapWords = 50) {
  if (!text || !text.trim()) return [];

  // Split into paragraphs first
  const paragraphs = text
    .split(/\n\s*\n+/)
    .map(p => p.trim())
    .filter(Boolean);

  const chunks = [];
  let currentWords = [];
  let currentWordCount = 0;

  for (const para of paragraphs) {
    const paraWords = para.split(/\s+/).filter(Boolean);

    // If adding this paragraph would exceed chunk size and we already have content
    if (currentWordCount + paraWords.length > chunkWords && currentWordCount > 0) {
      // Save current chunk
      chunks.push(currentWords.join(' '));

      // Start next chunk with overlap from end of current
      const overlapStart = Math.max(0, currentWords.length - overlapWords);
      currentWords = currentWords.slice(overlapStart);
      currentWordCount = currentWords.length;
    }

    currentWords.push(...paraWords);
    currentWordCount += paraWords.length;

    // If current chunk is over limit (single huge paragraph), force-split
    while (currentWordCount >= chunkWords) {
      chunks.push(currentWords.slice(0, chunkWords).join(' '));
      const overlapStart = chunkWords - overlapWords;
      currentWords = currentWords.slice(overlapStart);
      currentWordCount = currentWords.length;
    }
  }

  // Last chunk
  if (currentWords.length > 0) {
    chunks.push(currentWords.join(' '));
  }

  return chunks.filter(c => c.trim().length > 0);
}

module.exports = { chunkText };
