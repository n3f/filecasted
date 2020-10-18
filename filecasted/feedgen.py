import click
import mimetypes
import pprint
import os.path
import urllib.parse

from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from feedgen.feed import FeedGenerator
from pathlib import Path
from typing import List


@dataclass(frozen=True)
class Feedgen:
    _input: List[Path]
    output: Path
    verbose: int
    base_url: str = 'https://example.com/'

    def create(self):
        '''
        Create the RSS/podcast file

        [Required fields](https://help.apple.com/itc/podcasts_connect/#/itcb54353390)
        [Example RSS](https://help.apple.com/itc/podcasts_connect/#/itcbaf351599)

        :return:
        '''
        if self.verbose > 0:
            click.echo(self)
        fg = FeedGenerator()
        fg.load_extension('podcast')

        # Required
        fg.podcast.itunes_category('Arts')
        fg.title('The Title')
        # fg.podcast.itunes_title('Test')
        image_url = f'{self.base_url}/folder.jpg'
        fg.image(image_url)
        fg.podcast.itunes_image(image_url)
        fg.description('Audiobook')
        fg.language('en-us')
        # Explicit options: yes/no/clean
        fg.podcast.itunes_explicit('clean')

        # Optional
        # fg.author({'name':'Filecasted', 'email':'filecasted@filecasted.com')
        fg.link({'href': self.base_url,
                 # atom required
                 'rel': 'alternate'})

        start = datetime.now(timezone.utc)

        for i, feed in enumerate(self._input):
            fe = fg.add_entry()
            # Required
            fe.title(feed.name)
            url = '/'.join([self.base_url,
                            urllib.parse.quote(os.path.relpath(feed, self.output.parent))])
            fe.enclosure(url=url,
                         length=str(os.path.getsize(feed)),
                         type=mimetypes.guess_type(feed.as_uri())[0])
            fe.pubDate(start + timedelta(hours=i))
            # Optional
            # fe.podcast.itunes_block(True)
            # description
            # duration
        if self.verbose > 1:
            click.echo(fg.rss_str(pretty=True))
        fg.rss_file(self.output.as_posix())

    def __str__(self):
        # return f'{self.input}:{self.output}')
        # props = tuple(f.name for f in fields(Feedgen))
        # return pprint.pformat({k: v for (k, v) in self.__dict__.items() if k in props})
        input_str = '\n        '.join([str(i) for i in self._input])
        output_str = str(self.output)
        return '\n'.join([
            f'Input:  {input_str}',
            f'Output: {output_str}'
        ])
