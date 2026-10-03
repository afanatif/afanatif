# Profile artwork

The profile uses original, repository-hosted graphics with a consistent ink, mint, cyan and warm-paper palette. The header animates signal movement through a small network while keeping the introduction readable.

## Assets

- `assets/hero.gif`: animated header, 80 frames, repeating signal motion.
- `assets/hero.png`: static header used for reduced-motion preferences.
- Six project cards: warehouse modeling, multimodal security, seismic ML, agent workflows, emergency coordination and federated vision.
- Two contact graphics and one footer.

The images are self-contained and do not rely on a third-party statistics or animation service.

## Regenerate

```bash
python -m pip install -r tools/requirements.txt
python tools/build_profile_assets.py
```

The renderer uses Pillow. It searches for Windows Segoe UI/Consolas or Linux DejaVu fonts, then falls back to the available default. The checked-in artwork was rendered with Segoe UI and Consolas.

Edit the project descriptions and labels in the renderer when refreshing the artwork. Update the matching README text and alt descriptions together. Keep source credentials, private datasets and personal account exports outside the repository.
