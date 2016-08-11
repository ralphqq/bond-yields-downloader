## bond-yields-downloader
This script downloads daily reports on the Philippine Dealing System's benchmark government securities rates found at http://www.pds.com.ph/index.html%3Fpage_id=15256.html.

Although the PDS reports page allow you to download the file in .csv format, the site currently doesn't support bulk downloads. So if you're looking for a way to do that without the mindless tedium of repetitive clicking, then you might find this script a bit useful.

## Requirements
This script runs on Python 2.7 and requires the following:

1. python-dateutil  (`pip install python-dateutil`)
2. requests  (`pip install requests`)
3. six  (already comes installed along with python-dateutils)

## Usage
Just cd to the project's root directory and run:

```
    $ python downloader.py
```

Then enter the desired date range on the user prompt that appears. To accept the defaults (the current date), just leave the items blank. To download just one report, enter the same date on both the start and end fields or simply enter the desired date on either field. Please make sure that you enter a date using conventional date formats.

## Output
The downloaded CSV files are saved in the `Downloads` directory of the project folder.

## License
[MIT License](https://opensource.org/licenses/MIT)

## Contributing
Please contribute to this project in whatever capacity. Thanks.