# Publishing and visibility guide

## Existing repository

This project is already public at [RamunasSab/cad-design-review](https://github.com/RamunasSab/cad-design-review). Do not reinitialize it or recreate an existing release tag when updating documentation.

- Keep About description focused on mechanical drawing review, tolerances, GD&T, stack-ups, and DFM.
- Use relevant topics that describe actual functionality; do not imply a native CAD add-in or an automated parser.
- Keep the homepage link directed to the maintained project website.
- Preserve the published v1.5.0 snapshot. Changes on main remain unreleased until a new release is intentionally published.

## Publish the prepared v1.6.0 release

Preparation is on the `release/v1.6.0` branch. The stable release remains v1.5.0 until publication.

1. Review the preparation pull request and confirm its CI checks pass.
2. Before tagging, update README's stable command and channel table to v1.6.0, remove its preparation notice and unreleased/main-only qualifiers for included features, and describe main as the development channel. Change the changelog v1.6.0 heading from prepared to its actual publication date and remove its preparation-only notice. Update the README changelog anchor accordingly.
3. Merge the reviewed preparation changes into main and check the final CI result.
4. Create a **new v1.6.0 tag** at that exact main commit; keep v1.5.0 unchanged.
5. Create a GitHub Release titled **CAD Design Review v1.6.0 — Review templates and dimension-chain checks**. Copy the text from [prepared release notes](docs/releases/v1.6.0.md), removing only the sentence explaining that its command becomes available after tagging.
6. Publish the release, then verify the tag-specific README, changelog, install command, and source archives. The prepared notes' comparison link resolves after the tag exists.
7. Confirm the stable/main distinction still matches the published state.

No automatic release or tag creation is configured by this preparation. A custom ZIP is not required.

## Release checklist

1. Review the diff from the previous tag and complete relevant checks.
2. Move only the changes being released out of the Unreleased changelog section into a new version section.
3. Align version references in the skill metadata and README with the intended release.
4. Prepare a concise release title, user-visible changes, installation guidance, and known limitations.
5. Use tag-specific README and CHANGELOG links for reproducible documentation.
6. Create a new tag/release only when that release is ready. Do not move an existing tag.
7. Update the stable installation command and channel table after publication.

A separate ZIP asset is optional; GitHub provides source archives. Add a custom package only if its layout and contents have been checked.

## GitHub social preview

The public repository metadata on **2026-11-10** advertised a custom image from repository-images.githubusercontent.com, rather than the default generated card. This confirms configuration, not a visual quality review of the image.

To replace it, use repository **Settings → Social preview → Edit**. Upload a PNG, JPG, or GIF under 1 MB; GitHub recommends 1280 × 640 px for best display. Keep the title and key artwork away from the edges and check contrast on common link-preview backgrounds.

Reference: [GitHub social preview documentation](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/customizing-your-repositorys-social-media-preview).

## skills.sh visibility

The [project listing](https://skills.sh/ramunassab/cad-design-review/cad-design-review) was publicly reachable on **2026-11-10** and reported **1 install**. Counts are a point-in-time observation and may change.

The listing also displayed **“No SKILL.md available for this skill.”** The repository's [root SKILL.md](https://github.com/RamunasSab/cad-design-review/blob/main/SKILL.md) is publicly readable. Follow-up diagnostics on 2026-11-10: anonymous raw access returned HTTP 200, the GitHub tree identifies root SKILL.md as a regular file (mode 100644), and the official CLI supports root-level skills. The project's `/api/download/ramunassab/cad-design-review/cad-design-review` returned HTTP 404 with `not_found`; the same API for `vercel-labs/skills/find-skills` returned HTTP 200 with SKILL.md content. This establishes that the project's content snapshot is unavailable through the public API, while its listing exists. The internal ingestion/cache failure cause is not established. Do not rearrange or duplicate the repository skill solely on this evidence.

The maintainers' replies on [issue #1073](https://github.com/vercel-labs/skills/issues/1073) and [issue #2367](https://github.com/vercel-labs/skills/issues/2367) state that a normal installation with telemetry enabled triggers indexing; they do not promise a specific refresh time or guarantee it fixes every missing snapshot. The CLI install event includes a skill-to-repository-file-path map.

Follow-up:

1. Recheck whether the listing displays the skill instructions after the directory refreshes.
2. If the issue persists, prepare a report for the Skills maintainers with the listing URL, root SKILL.md URL, default branch, and observed message.
3. Verify real installation on a machine with npm/GitHub access when available; a directory rendering issue alone does not prove installation failure.
4. Keep the README directory link and install-count badge pointed at the existing source.

The [official directory documentation](https://skills.sh/docs) describes install-based ranking and this badge format:

```markdown
[![skills.sh](https://skills.sh/b/ramunassab/cad-design-review)](https://skills.sh/ramunassab/cad-design-review/cad-design-review)
```

Use ordinary, genuine installations for validation. Do not generate repeat installs merely to inflate ranking. A low count does not measure engineering quality.

## After sharing

Link to the README quick start and a concrete worked example. Recheck the GitHub preview and directory listing, and distinguish visits/install counts from successful user reviews.
