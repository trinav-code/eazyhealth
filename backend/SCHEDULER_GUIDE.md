# Automated Briefing Generation Guide

## Overview

The scheduler automatically generates health briefings on a rotating schedule to provide fresh content without redundancy.

## Schedule

### Data Analysis (2x/week)
- **Monday**: Rotating reading level (Week 1: Grade 6, Week 2: Grade 8, Week 3: High School, Week 4: College)
- **Thursday**: Complementary reading level to Monday's

### Article Summaries (Mon-Fri, 1x/day)
- **Monday**: Grade 6
- **Tuesday**: Grade 8
- **Wednesday**: High School
- **Thursday**: College
- **Friday**: Grade 3

**Total: 7 posts/week**

## Manual Testing

To test the scheduler manually:

```bash
cd backend

# Make sure backend server is running in another terminal
# Then run:
python3 scheduler.py
```

This will generate briefings based on the current day of the week.

## Automatic Scheduling (Cron Job)

### Set up cron job (macOS/Linux):

1. Open crontab editor:
   ```bash
   crontab -e
   ```

2. Add this line to run daily at 6:00 AM:
   ```bash
   0 6 * * * cd /Users/trinav/personal/eazyhealth/backend && /usr/bin/python3 scheduler.py >> /tmp/eazyhealth-scheduler.log 2>&1
   ```

3. Save and exit (`:wq` in vim)

4. Verify cron job is installed:
   ```bash
   crontab -l
   ```

### View scheduler logs:
```bash
tail -f /tmp/eazyhealth-scheduler.log
```

## Schedule Breakdown

### Week 1 (4-week cycle)
- **Monday**: Data Analysis (Grade 6) + Article (Grade 6)
- **Tuesday**: Article (Grade 8)
- **Wednesday**: Article (High School)
- **Thursday**: Data Analysis (High School) + Article (College)
- **Friday**: Article (Grade 3)

### Week 2
- **Monday**: Data Analysis (Grade 8) + Article (Grade 6)
- **Thursday**: Data Analysis (College) + Article (College)
- (Tues/Wed/Fri same as Week 1)

### Week 3
- **Monday**: Data Analysis (High School) + Article (Grade 6)
- **Thursday**: Data Analysis (Grade 6) + Article (College)
- (Tues/Wed/Fri same as Week 1)

### Week 4
- **Monday**: Data Analysis (College) + Article (Grade 6)
- **Thursday**: Data Analysis (Grade 8) + Article (College)
- (Tues/Wed/Fri same as Week 1)

## Article Topics

Topics rotate through a curated list:
- Diabetes management
- Heart health and cardiovascular disease
- Mental health and wellness
- Nutrition and healthy eating
- Vaccine safety and effectiveness
- Cancer prevention and screening
- Sleep and health
- Exercise and physical activity
- Antibiotic resistance
- Maternal and child health

## Troubleshooting

### Scheduler fails to generate briefings:
1. Make sure backend server is running (`http://localhost:8000`)
2. Check that you have valid API keys in `.env`
3. Check logs: `tail -f /tmp/eazyhealth-scheduler.log`

### Duplicate slug errors:
- The scheduler may occasionally generate briefings with duplicate slugs
- This is expected and will be skipped
- The system will try again the next day

## Customization

### Change schedule times:
Edit the cron job time (first two numbers):
- `0 6` = 6:00 AM
- `0 18` = 6:00 PM
- `30 9` = 9:30 AM

### Change rotation:
Edit `scheduler.py`:
- `DATA_ANALYSIS_LEVELS`: Change reading level rotation
- `ARTICLE_LEVELS_BY_DAY`: Change daily article reading levels
- `ARTICLE_TOPICS`: Add/remove topics

### Disable automation:
```bash
crontab -e
# Comment out or delete the scheduler line
# Save and exit
```

## Future Enhancements

Potential improvements:
- Database-backed topic tracking to avoid recent duplicates
- Smarter slug generation to prevent collisions
- Email notifications when generation fails
- Web dashboard to view/manage schedule
- Integration with real data sources (CDC APIs, etc.)
