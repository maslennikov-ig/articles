# Publish a ready Telegram post through Content Factory

Writing and editing requests follow the venue's editorial and image workflow.
For an explicit request to publish, use the final text, photos and destination
chosen by the author. When the author supplies a ready post, carry its wording
and links into the payload as approved. For a new draft or a changed version,
show the full final text, photo placement and destination before asking to send.

## Choose the layout before preparing the send

- Use `format: "rich"` by default for authored posts and announcements. Convert
  the title to `<h1>` and real section titles to `<h2>`–`<h6>`. Preserve a title-free
  post when intended. Use `<ul>` or `<ol>` with `<li>` for actual lists and
  `<strong>` for emphasis within text. The `rich` flag alone cannot turn a bold
  paragraph into a sized heading. For an author-supplied ready post, preserve
  its wording and intended structure.
- Pass owned assets as `mediaIds`. For an image near its discussion, place
  `<figure><img src="tg://photo?id=media_1"/><figcaption>Caption</figcaption></figure>`
  between the relevant text blocks. The slot is the 1-based position in
  `mediaIds`. Map every supplied ID once when using explicit positions. Use
  `<tg-collage>` or `<tg-slideshow>` when the photos belong together.
- Check the live tool's `html` description before using these features.
  The updated connector advertises `tg://photo?id=media_1`. Older versions
  append all photos at the end and remove image tags from input. If only an
  older connector is available, keep the inline draft and show the actual
  end collage as an alternative for author approval.
- Use `format: "caption"` when the author wants a classic photo or album with
  a caption. The caption has a 1024 visible character limit and flattens heading
  sizes. Pass the format explicitly because MCP defaults to `caption`.

For an extended post, choose only blocks that help the reader: expandable
quotes and `<details>`, native lists and checkboxes, tables, code, math, maps,
anchors, spoilers, or section illustrations. See the
[official Rich HTML examples](https://core.telegram.org/bots/api#rich-message-formatting-options).
Use `<video src="tg://video?id=media_2"></video>` for an owned MP4 or GIF,
`<audio src="tg://audio?id=media_2"></audio>` for owned audio, or
`<tg-document src="tg://document?id=media_2"></tg-document>` for a workspace
document. Supply an existing asset or import it through the supported media
library route. Direct media URLs and local paths do not go into the payload.
Channel buttons can open a link, copy text or be disabled. Bot workflows such
as callback handlers, login and Mini Apps require separate integration.
The connector maps the slots to Telegram's
[InputRichMessage.media](https://core.telegram.org/bots/api#inputrichmessagemedia).

## Send through Content Factory MCP

1. Find the Content Factory MCP tools in the current chat. Use `channels_list`
   to match the author's destination to an active Telegram channel in the
   connected workspace. If the tools, workspace or channel are unavailable,
   keep the post ready and explain what needs to be connected or selected. For
   MCP setup, use the connector details in Content Factory's approved-apps settings.
2. Use up to ten owned workspace assets. Find existing assets with
   `media_library` and verify them with `media_inspect`. For an authorized
   local photo, use the `photo` argument of `media_upload` when advertised.
   Generate a fresh base64url proof from 32 random bytes. Keep it local and send
   only `name` (basename), `size`, `sha256` (of the file), and
   `uploadProofSha256` (of the proof string) to MCP. Use lowercase hex hashes.
   Verify that `uploadUrl` is the upload endpoint on the configured Content
   Factory origin. POST the multipart field `file` with
   `Accept: application/json; cf-upload-ticket=<proof>`, without following
   redirects. Keep the proof out of tool arguments, logs and process argv.
   Use `media_upload_status` for the same session, including after a lost
   HTTP response. Collect `media.mediaId` only when the status is `ready`.
   The argument-free upload widget and media library are available when a
   person chooses the file directly.
3. Convert the final text to HTML using `<p>` and `<br>` for paragraphs and
   breaks, `<u>` for underline and `<a href="https://…">` for links. Before
   requesting confirmation, inspect the exact `html`, `format` and ordered
   `mediaIds` against the reviewed layout. A titled news post should begin
   with `<h1>…</h1>` in the payload. Check photo presence and actual placement
   separately from the heading markup. Map each `media_N` to the exact file
   and show its position in the review preview. Without explicit positions,
   one photo or an ordered collage follows the text.
4. For immediate publication, call `telegram_publish_ready` with `requestId`
   (one UUID for this publication), `channelId`, `html`, `format` and the
   ordered `mediaIds`. Omit `mediaIds` for rich text without attachments. Use
   `coverMediaId` only for compatibility with a one-photo caption.
   Present the returned confirmation question to the author. Once they confirm,
   repeat the call with identical arguments plus the returned `confirmation`.
   Follow any approval prompt shown by the chat host. A request to schedule for
   later does not authorize this immediate-send tool.
5. After queuing or a timeout, read `telegram_publication_status` with the same
   `requestId`. Keep that UUID while resolving the outcome to avoid a duplicate.
   Report publication with `telegramUrl` once the receipt says `PUBLISHED` and
   contains the link. Report the actual status while delivery is pending or failed.
   If checking the rendered layout, use the Telegram app: the public web
   preview may only show an invitation to open it. The receipt verifies
   delivery. To adjust a delivered post, use a supported edit operation for
   the same message with current authorization. The ready-post MCP tool
   creates messages only.
