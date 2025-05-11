# AEye Vision QC — Feature Roadmap & Technical Notes

## ✅ Current Features
- Image capture with optional camera ID logging
- Sample and master separation with clean filenames
- DeltaE comparison using LAB color space
- CSV logging for traceability
- Modular code structure for capture/comparison

---

## 🔁 Planned Features

- [ ] **Fast scan mode** (skip image saving, log only LAB data)
- [ ] Optional audit image saving (with flag or UI checkbox)
- [ ] Auto-rotate/purge audit images older than X days
- [ ] Crop image to region-of-interest (ROI) before analysis
- [ ] Automatically define ROI (center crop or HSV masking)
- [ ] **Highlight or outline the scanned ROI** in the UI preview
- [ ] Append LAB values and results to CSV logs
- [ ] Pull latest samples in UI by date, ID, or result
- [ ] Filter by PASS/FAIL in UI (live dashboard)
- [ ] Support dual-camera kiosk setup
- [ ] Generate basic QA reports (PDF or export to Excel)