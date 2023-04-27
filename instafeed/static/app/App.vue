<template>

    <div id="container">
        <div id="navBar">
            <button id="btn_connect" style="display: flex; gap:5px" @click="connect_instagram">
                <font-awesome-icon :icon="['fab', 'instagram']"/>
                <p>Connect with Instagram</p>
            </button>
            <div style="display: flex"><p v-if="username">Connected to {{ username }} with instagram</p>
                <p>Change account</p></div>
            <div></div>
            <div>
                <button></button>
                <button></button>
                <button></button>
                <button></button>
            </div>
        </div>
        <div id="content">
            <div id="content-left">
                <label>
                    <b>FEED TITLE</b>
                </label>
                <input v-model="feed_title"/>
                <div class="line">
                    <div>
                        <b>POST SPACING</b>
                        <select v-model="post_spacing">
                            <option v-for="option in post_spacing_options" :value="option">
                                {{ option.name }}
                            </option>
                        </select>
                    </div>
                    <div>
                        <label>
                            <b>ON POST CLICK</b>
                        </label>
                        <select v-model="on_post_click">
                            <option v-for="option in on_post_click_options" :value="option">
                                {{ option }}
                            </option>
                        </select>
                    </div>
                </div>
                <div class="line">
                    <div><label>
                        <b>LAYOUT</b></label>
                        <select v-model="layout">
                            <option v-for="option in layout_options" :value="option">
                                {{ option }}
                            </option>
                        </select>
                    </div>
                    <div>
                        <label><b>CONFIGURATION</b></label>
                        <select v-model="configuration">
                            <option v-for="option in configuration_options" :value="option">
                                {{ option }}
                            </option>
                        </select>
                    </div>
                </div>
                <div v-if="layout=='Slider-Squares'||layout=='Slider-Tiles'" class="line">
                    <div>
                        <label><b>IMAGES PER SLIDE</b></label>
                        <input v-model="temp.per_slide" type="number" min="0">
                    </div>
                    <div>
                        <label><b>NUMBER OF POSTS</b></label>
                        <input v-if="configuration=='Auto'" disabled placeholder="Auto" id="auto">
                        <input v-else="" v-model="number_of_posts" type="number" min="0" max="10">
                    </div>
                </div>
                <div v-else class="line">
                    <div>
                        <label><b>NUMBER OF ROWS</b></label>
                        <input v-model="number_of_rows" type="number" min="0">
                    </div>
                    <div>
                        <label><b>NUMBER OF COLUMNS</b></label>
                        <input v-if="configuration=='Auto'" disabled placeholder="Auto" id="auto">
                        <input v-else="" v-model="number_of_columns" type="number" min="0" max="10">
                    </div>
                </div>
                <div class="line">
                    <div>
                        <label><b>SLIDER PAGES-MOBILE</b></label>
                        <input v-model="slider_pages_mobile" min="0" type="number">
                    </div>
                    <div>
                        <label><b>NUMBER OF POSTS-MOBILE</b></label>
                        <input v-model="number_of_post_mobile" min="0" max="10" type="number">
                    </div>
                </div>
                <div class="line">
                    <div>
                        <label><b>SHOW LIKES</b></label>
                        <select v-model="show_likes">
                            <option v-for="option in show_likes_options" :value="option">
                                {{ option.name }}
                            </option>
                        </select>
                    </div>
                    <div>
                        <label><b>SHOW FOLLOWERS</b></label>
                        <select v-model="show_followers">
                            <option v-for="option in show_followers_options" :value="option">
                                {{ option.name }}
                            </option>
                        </select>
                    </div>
                </div>
                <div class="line">
                    <div>
                        <label><b>POST TO SHOW</b></label>
                        <select v-model="post_to_show"></select>
                    </div>
                    <div>
                        <label><b>VIDEOS AUTOPLAY</b></label>
                        <select v-model="videos_autoplay"></select>
                    </div>
                </div>
                <div>
                    <label><b>AUTOMATIC PRODUCT FEED</b></label>
                    <select v-model="automatic_product_feed">
                        <option> hello</option>
                    </select>
                </div>
                <div>
                    <label><b>FILTER BY HASHTAGS</b></label>
                    <input placeholder="Leave empty to show all post"/>
                </div>
                <button id="btn_save">Save feed</button>
            </div>
            <div id="content-right">
                <label id="preview">
                    <b>PREVIEW</b>
                </label>
                <hr>
                <br>
                <div id="insta_feed">
                    <div id="feed_title">{{ feed_title }}</div>
                    <div v-if="layout=='Grid-Tiles'||layout=='Grid-Squares'" id="images" :style="{
                        display: 'grid',
                        gap: post_spacing.value +'px',
                        gridTemplateColumns: 'repeat('+number_of_columns+',1fr)'
                    }">
                        <template v-for="(image,index) in images">
                            <div v-if="index<number_of_grid_posts" class="square" :style="{
                               aspectRatio: ratio
                        }">
                                <div class="square-content">
                                    <img :style="{
                                    width: '100%',
                                    height: '100%'
                        }" :src="image.url">
                                </div>
                            </div>
                        </template>
                    </div>
                    <image_slider v-else :gap="post_spacing" :ratio="ratio" :images="images" :proptemp="temp"/>
                </div>
            </div>
        </div>
    </div>
    <div>
        Hello World
    </div>
    <div>
        <div id="fb-root"></div>
        <div class="fb-login-button" data-width="1000px" data-size="" data-button-type="" data-layout=""
             data-auto-logout-link="true" data-use-continue-as="false"></div>
        <div id="user_data"></div>
    </div>
</template>

<script>
import axios from 'axios'
import Image_slider from "./components/image_slider.vue";

export default {
    name: "App",
    components: {Image_slider},
    computed: {
        square() {
            return this.layout == 'Grid-Squares' || this.layout == 'Slider-Squares'
        },
        images() {
            return this.allImages.filter((image, index) => index < this.number_of_posts)
        },
        ratio: function () {
            if (this.square) {
                return 1 / 1
            } else {
                return 2 / 3
            }
        },
        number_of_grid_posts() {
            if (this.layout == 'Grid-Tiles' || this.layout == 'Grid-Squares') {
                console.log(this.number_of_posts)
                return this.number_of_rows * this.number_of_columns
            }
        }
    },
    data() {
        return {
            allImages: [{url: "https://scontent.cdninstagram.com/v/t51.29350-15/342536984_195912416563790_8294471644719006521_n.jpg?_nc_cat=108&ccb=1-7&_nc_sid=8ae9d6&_nc_ohc=t9Ea0zHtnggAX_PHZ-Y&_nc_ht=scontent.cdninstagram.com&edm=ANQ71j8EAAAA&oh=00_AfAAik2TcttAUfHVRLJNwoIntn8An3sGX3_IxXKHVSmZaA&oe=644D572C", alt: "Image 1"},
                {url: "/bought_together/static/app/img/img_5.jpg", alt: "Image 2"},
                {url: "/bought_together/static/app/img/img_2.png", alt: "Image 3"},
                {url: "/bought_together/static/app/img/img_3.png", alt: "Image 4"},
                {url: "/bought_together/static/app/img/img_5.jpg", alt: "Image 5"},
                {url: "/bought_together/static/app/img/img_3.png", alt: "Image 6"},
                {url: "/bought_together/static/app/img/img_2.png", alt: "Image 7"},
            ],
            image_width: 200,
            username: '',
            feed_title: 'Hello World',
            post_spacing: {
                name: 'Medium',
                value: 20
            },
            on_post_click: 'Open popup/show product',
            layout: 'Grid-Tiles',
            configuration: 'Auto',
            number_of_posts: 7,
            temp: {
                per_slide: 3,
            },
            slider_pages_mobile: 3,
            number_of_post_mobile: 3,
            number_of_rows: 3,
            number_of_columns: 3,
            show_likes: {name: 'Yes', value: true},
            show_followers: {name: 'Yes', value: true},
            post_to_show: 'All',
            videos_autoplay: '',
            automatic_product_feed: '',
            filter_by_hashtags: '',
            post_spacing_options: [
                {
                    name: 'No spacing',
                    value: 0
                }
                , {
                    name: 'Small',
                    value: 10
                }
                ,
                {
                    name: 'Medium',
                    value: 20
                }
                , {
                    name: 'Large',
                    value: 30
                }
            ],
            on_post_click_options: ['Open popup/show product', 'Go to instagram', 'Do nothing'],
            layout_options: ['Grid-Squares', 'Grid-Tiles', 'Slider-Squares', 'Slider-Tiles'],
            configuration_options: ['Manual', 'Auto'],
            show_likes_options: [{name: 'Yes', value: true}, {name: 'No', value: false}],
            show_followers_options: [{name: 'Yes', value: true}, {name: 'No', value: false}]
        }
    },
    methods: {
        connect_instagram() {
            window.location.href = '/instafeed/connect'
        }
    },
    mounted() {
        let self = this
        console.log("Hello shopify")
        axios.get('/instafeed/get/insta_user').then((res) => {
            self.username = res.data.username
        })
    }

}

</script>
<style>
label {
    display: block;
    color: #212b35;
    font-weight: 400;
}


input {
    margin-bottom: 24px !important;
    flex: 1;
    text-size-adjust: 100%;
    fill: currentColor;
    -webkit-font-smoothing: antialiased;
    -webkit-box-direction: normal;
    font: inherit;
    padding: .5rem 1rem;
    background-color: #fff;
    border: .1rem solid #c4cdd5;
    border-radius: .3rem;
    color: #31373d;
    display: block;
    font-size: 1.6rem;
    width: 100%;
    line-height: 2.4rem;
    min-width: 7.5rem;
    vertical-align: baseline;
    height: auto;
    margin: 0;
    max-width: 100%;
    font-family: -apple-system, blinkmacsystemfont, san francisco, roboto, segoe ui, helvetica neue, sans-serif;
    box-shadow: 0 0 0 1px transparent, 0 1px 0 0 rgba(22, 29, 37, .05);
    box-sizing: border-box;
    transition: box-shadow .2s cubic-bezier(.64, 0, .35, 1);
    appearance: none;
    min-height: 3.4rem;
}

select {
    padding: 10px;
    background-size: 21px 21px;
    background-repeat: no-repeat;
    box-shadow: 0 0 0 1px transparent, 0 1px 0 0 rgba(22, 29, 37, .05);
    text-size-adjust: 100%;
    fill: currentColor;
    -webkit-font-smoothing: antialiased;
    -webkit-box-direction: normal;
    font: inherit;
    text-transform: none;
    position: relative;
    background-color: #fff;
    border: .1rem solid #c4cdd5;
    border-radius: .3rem;
    color: #31373d;
    display: block;
    width: 100%;
    font-size: 1.6rem;
    line-height: 2.4rem;
    min-width: 7.5rem;
    vertical-align: baseline;
    height: auto;
    margin: 0;
    max-width: 100%;
    font-family: -apple-system, blinkmacsystemfont, san francisco, roboto, segoe ui, helvetica neue, sans-serif;
    box-sizing: border-box;
    transition: box-shadow .2s cubic-bezier(.64, 0, .35, 1);
    appearance: none;
    min-height: 3.4rem;
    padding-right: 3.2rem;
    background-image: url(data:image/svg+xml;charset=utf8;base64,PHN2ZyB4bWxucz0naHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmcnIHZpZXdCb3g9JzAgMCAyMCAyMCc+PHBhdGggZmlsbD0ncmdiKDk5LDExNSwxMjkpJyBkPSdNMTMgOGwtMy0zLTMgM2g2em0tLjEgNEwxMCAxNC45IDcuMSAxMmg1Ljh6JyBmaWxsLXJ1bGU9J2V2ZW5vZGQnPjwvcGF0aD48L3N2Zz4=);
    background-position: right .7rem top .7rem;
}

option {
    font-weight: normal;
    display: block;
    white-space: nowrap;
    min-height: 1.2em;
    padding: 10px;
}

.line {
    display: flex;
    width: 100%;
    height: auto;
    margin-bottom: 1.5rem;
    text-align: left;
    gap: 20px
}

.line div {
    width: 100%;
    flex: 1;
}


#container {
    background-color: #f4f6f8;
    padding: 20px 10px;
}

#navBar {
    box-shadow: 0 0 0 1px rgba(63, 63, 68, .05), 0 1px 3px 0 rgba(63, 63, 68, .15);
    margin-bottom: 2rem;
    background-color: #ffffff;
    padding: 20px;
}

#btn_connect {
    color: #ffffff;
    align-items: center;
    flex-wrap: wrap !important;
    border-radius: 4px;
    background: rgb(0 128 96);
    border: 0.1rem solid transparent;
    box-shadow: inset 0 1px 0 0 transparent, 0 1px 0 0 rgb(22 29 37/5%), 0 0 0 0 transparent;
    font-weight: 400;
    margin: 3px;
    display: inline-block;
    justify-content: center;
    padding: 7px 16px;
    cursor: pointer;
    white-space: nowrap;
    text-transform: none;
    font-family: -apple-system, blinkmacsystemfont, san francisco, roboto, segoe ui, helvetica neue, sans-serif;
}

#btn_connect p {

}

#content {
    display: flex;
}

#content-left {
    text-size-adjust: 100%;
    text-rendering: optimizeLegibility;
    font-size: 1.4em;
    line-height: 2rem;
    font-weight: 400;
    font-family: -apple-system, blinkmacsystemfont, san francisco, roboto, segoe ui, helvetica neue, sans-serif;
    fill: currentColor;
    text-transform: initial;
    letter-spacing: initial;
    -webkit-font-smoothing: antialiased;
    text-align: left;
    -webkit-box-direction: normal;
    float: left;
    display: inline-block;
    color: #1a1919;
    box-sizing: border-box;
    padding: 2rem;
    background-color: #fff;
    border-radius: .3rem;
    box-shadow: 0 0 0 1px rgba(63, 63, 68, .05), 0 1px 3px 0 rgba(63, 63, 68, .15);
    margin-bottom: 2rem;
    margin-left: 0;
    flex: 1;
}

#btn_save {
    text-size-adjust: 100%;
    -webkit-font-smoothing: antialiased;
    -webkit-box-direction: normal;
    font: inherit;
    overflow: visible;
    position: relative;
    display: inline-block;
    min-height: 3.6rem;
    min-width: 3.6rem;
    padding: .7rem 1.6rem;
    color: #fff;
    fill: #fff;
    line-height: normal;
    text-align: center;
    text-decoration: none;
    transition-property: background, border, box-shadow;
    transition-duration: .2s;
    transition-timing-function: cubic-bezier(.64, 0, .35, 1);
    box-sizing: border-box;
    cursor: pointer;
    white-space: nowrap;
    text-transform: none;
    font-family: -apple-system, blinkmacsystemfont, san francisco, roboto, segoe ui, helvetica neue, sans-serif;
    vertical-align: middle;
    user-select: none;
    -webkit-appearance: none;
    -webkit-tap-highlight-color: transparent;
    border-radius: 4px;
    background: rgb(0 128 96);
    border: .1rem solid transparent;
    box-shadow: inset 0 1px 0 0 transparent, 0 1px 0 0 rgb(22 29 37/5%), 0 0 0 0 transparent;
    font-weight: 400;
    margin: 3px;
    width: 100%;
}

#content-right {
    text-size-adjust: 100%;
    text-rendering: optimizeLegibility;
    font-size: 1.4em;
    line-height: 2rem;
    font-weight: 400;
    font-family: -apple-system, blinkmacsystemfont, san francisco, roboto, segoe ui, helvetica neue, sans-serif;
    fill: currentColor;
    text-transform: initial;
    letter-spacing: initial;
    -webkit-font-smoothing: antialiased;
    text-align: left;
    -webkit-box-direction: normal;
    float: left;
    margin-left: 2%;
    display: inline-block;
    color: #1a1919;
    box-sizing: border-box;
    padding: 2rem;
    background-color: #fff;
    border-radius: .3rem;
    box-shadow: 0 0 0 1px rgba(63, 63, 68, .05), 0 1px 3px 0 rgba(63, 63, 68, .15);
    margin-bottom: 2rem;
    flex: 2;
}

#preview {
    display: block;
    color: #212b35;
    font-weight: 400;
}

#insta_feed {
    overflow: hidden;

    text-size-adjust: 100%;
    text-rendering: optimizeLegibility;
    font-size: 1.4em;
    line-height: 2rem;
    font-weight: 400;
    font-family: -apple-system, blinkmacsystemfont, san francisco, roboto, segoe ui, helvetica neue, sans-serif;
    fill: currentColor;
    text-transform: initial;
    letter-spacing: initial;
    -webkit-font-smoothing: antialiased;
    -webkit-box-direction: normal;
    color: #1a1919;
    display: block;
    text-align: center;
    clear: both;
    margin: 30px auto 0;
    margin-bottom: 20px;
    margin-top: 15px;
    position: relative;
    padding: 0px 20px;
}

#feed_title {
    margin-bottom: 30px;
    text-align: center;
}

#images {
    justify-content: center;
    position: relative;
}

#auto {
    text-size-adjust: 100%;
    fill: currentColor;
    -webkit-font-smoothing: antialiased;
    -webkit-box-direction: normal;
    font: inherit;
    position: relative;
    padding: .5rem 1rem;
    border-radius: .3rem;
    display: block;
    width: 100%;
    font-size: 1.6rem;
    line-height: 2.4rem;
    min-width: 7.5rem;
    vertical-align: baseline;
    height: auto;
    margin: 0;
    max-width: 100%;
    font-family: -apple-system, blinkmacsystemfont, san francisco, roboto, segoe ui, helvetica neue, sans-serif;
    box-shadow: 0 0 0 1px transparent, 0 1px 0 0 rgba(22, 29, 37, .05);
    box-sizing: border-box;
    transition: box-shadow .2s cubic-bezier(.64, 0, .35, 1);
    appearance: none;
    min-height: 3.4rem;
    cursor: not-allowed;
    background-color: #f4f6f8;
    border: .1rem solid #dfe4e8;
    color: #c4cdd5;
}

body {

}
</style>