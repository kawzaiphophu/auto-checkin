# HR Attendance Automation

Automated HR attendance system using Selenium and GitHub Actions.

## Setup

### For Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the script:
```bash
python hr_attendance.py
```

### For GitHub Actions

1. Push this repository to GitHub

2. Add GitHub Secret:
   - Go to your repository → Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Name: `HR_TOKEN`
   - Value: Your JWT token

3. Enable GitHub Actions:
   - Go to Actions tab
   - Enable workflows if prompted

4. The workflow will run automatically at 9:00 AM daily (Bangkok time)
   - You can also trigger it manually from the Actions tab

## Schedule

- **GitHub Actions**: Runs daily at 9:00 AM (Bangkok time / UTC+7)
- **Local (macOS)**: Runs every 30 seconds via launchd

## Files

- `hr_attendance.py` - Main attendance script
- `requirements.txt` - Python dependencies
- `.github/workflows/attendance.yml` - GitHub Actions workflow
- `com.hr.attendance.plist` - macOS launchd configuration

## Logs

- GitHub Actions logs are available in the Actions tab
- Local logs: `~/hr_attendance/attendance.log`
