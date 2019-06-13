from linebot.models import (
    PostbackTemplateAction, CarouselColumn
)

column1 = CarouselColumn(
                    thumbnail_image_url='https://i.ibb.co/tHbT4Hd/pecu.jpg',
                    title='我愛蔡芸琤老師~',
                    text='💕💕💕',
                    actions=[
                        PostbackTemplateAction(
                            label='點我點我',
                            text='LOVE U',
                            data='love_pecu'
                        )
                    ]
                )
column2 = CarouselColumn(
                    thumbnail_image_url='https://i.ibb.co/2MpL9HS/shi.jpg',
                    title='我愛石百達老師~',
                    text='💕💕💕',
                    actions=[
                        PostbackTemplateAction(
                            label='點我點我',
                            text='LOVE U',
                            data='love_shi'
                        )
                    ]
                )
