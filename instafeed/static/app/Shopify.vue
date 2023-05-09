<template>
    <div>Hello</div>
    <div id="insta_feed">
        <div id="feed_title">{{ feed_title }}</div>
        <div v-if="layout.includes('Grid')" id="images" :style="{
                        display: 'grid',
                        gap: post_spacing.value +'px',
                        gridTemplateColumns: 'repeat('+number_of_columns+',1fr)'
                    }">
            <template v-for="(image,index) in allImages">
                <div v-if="index<number_of_grid_posts"
                     :style="{
                               aspectRatio: ratio,
                               position: 'relative',
                        }" @mouseenter="image.hover=true"
                     @mouseleave="image.hover=false">
                    <img v-if="image.media_type=='IMAGE'" :style="{
                                    width: '100%',
                                    height: '100%'
                        }" :src="image.media_url" :alt="image.caption">
                    <img v-if="image.media_type=='VIDEO'" :style="{
                                    width: '100%',
                                    height: '100%'
                        }" :src="image.thumbnail_url" :alt="image.caption">
                    <div class="post_hover" v-if="image.hover&&image.media_type=='IMAGE'"
                         @click="show_post(image)">
                        <font-awesome-icon icon="fa-brands fa-instagram"
                                           style="color: white; height: 15%; width: 15%"/>
                    </div>
                    <div class="post_hover" v-if="image.hover&&image.media_type=='VIDEO'"
                         @click="show_post(image)">
                        <font-awesome-icon icon="fa-solid fa-play"
                                           style="color: white; height: 15%; width: 15%"
                        />
                    </div>
                </div>
            </template>
        </div>
        <image_slider v-else @show_post="show_post" :gap="post_spacing" :ratio="ratio" :images="images"
                      :proptemp="temp"/>
        <Modal style="width: 70%; height: auto;"
               :footer="null"
               v-model:visible="post_modal"
               :maskClosable="false"
               @cancel="post_modal=false">
            <div style="display: flex">
                <img v-if="selected_post.media_type == 'IMAGE'"
                     :src="selected_post.media_url"
                     :alt="selected_post.caption"
                     style="width: 50%; height: 50%">
                <video height="400" autoplay v-if="selected_post.media_type == 'VIDEO'">
                    <source :src="selected_post.media_url">
                </video>
                <div style="width: 100%; display: flex; flex-direction: column">
                    <div style="margin-left:20px; display: flex; background-color: white; align-items: center;border-bottom: 1px solid #dcdcdc;">
                        <div style="display: flex; justify-content: center; align-items: center;border: 1px solid #E2E2E2; border-radius: 50%; height: 40px; width: 40px">
                            <font-awesome-icon icon="fa-brands fa-instagram"
                                               style="height:30px; width: 30px; color: black"/>
                        </div>
                        <div @click="redirectToInstagramUser"
                             style="cursor: pointer; color: #000; font-weight: 600; line-height: 23px; font-size: 17px; margin-left: 15px">
                            {{ username }}
                            <div v-if="show_followers.value"
                                 style="color: #000; font-weight: 400;font-size: 13px;">
                                {{ followers_count }} Followers
                            </div>
                        </div>
                    </div>
                    <div class="controls">
                        <font-awesome-icon @click="prev_slide" :icon="['fas', 'chevron-left']"/>
                        <font-awesome-icon @click="next_slide" :icon="['fas', 'chevron-right']"/>
                    </div>
                    <div v-if="selected_post.caption" style="margin: 10px 0px 10px 25px">{{
                        selected_post.caption
                        }}
                    </div>
                    <div style="display: flex;gap: 20px; margin-bottom: 20px">
                        <div v-if="show_likes.value" style="margin: 10px 0px 0px 25px">
                            {{ selected_post.like_count }}
                            <font-awesome-icon icon="fa-regular fa-heart" beat style="color: black"/>
                        </div>
                        <div style="margin: 10px 0px 0px 25px">
                            {{ selected_post.comments_count }}
                            <font-awesome-icon :icon="['far', 'message']"/>
                        </div>
                    </div>
                    <div v-if="selected_post.comments" style="display: flex;flex-direction: column; gap: 10px">
                        <div v-for="comment in selected_post.comments.data"
                             style="margin: 0px 0px 0px 25px; display: flex;gap: 10px">
                            <b>{{ comment.from.username }}</b>
                            <p>{{ comment.text }}</p>
                        </div>
                    </div>
                    <div v-if="selected_post.list_tags"
                         style="height: 35%; text-align: center;width:100%;margin: 20px 25px 10px 25px;">
                        <template v-for="tag in selected_post.list_tags">
                            <div style="color: rgb(0, 0, 0);
                                        font-weight: 600;
                                        line-height: 23px;
                                        font-size: 17px;
                                        margin: 15px;">
                                {{ list_products.find(product => product.product_id == tag).name }}
                            </div>
                            <div style="margin: 20px;">
                                <img :src="list_products.find(product => product.product_id == tag).image_url"
                                     style="width: 80%;aspect-ratio: 1.2"/>
                            </div>
                            <button @click="handleShopNow(list_products.find(product => product.product_id == tag).handle)"
                            >Shop now
                            </button>
                        </template>
                    </div>
                </div>
            </div>
        </Modal>
    </div>
</template>

<script>
import axios from 'axios'
import Image_slider from "./components/image_slider.vue";
import {Modal} from "ant-design-vue";

export default {
    name: "App_extension",
    components: {Modal, Image_slider},
    computed: {
        square() {
            return this.layout.includes('Squares')
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
                if (this.number_of_rows * this.number_of_columns > this.allImages.length) {
                    return this.allImages.length
                } else return this.number_of_rows * this.number_of_columns
            }
        },
    },
    data() {
        return {
            followers_count: 0,
            allImages: [],
            post_modal: false,
            selected_post: {},
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
            // post_to_show: 'All',
            // videos_autoplay: '',
            // automatic_product_feed: '',
            // filter_by_hashtags: '',
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
    }
    ,
    mounted() {
        let self = this
        axios.post("apps/instaf/instafeed/show/feed", {shop_url: window.location.host}).then((res) => {
            console.log(res)
            self.username = res.data.result.user.username
            self.user_id = res.data.result.user_id
            self.followers_count = res.data.result.followers_count
            self.feed_title = res.data.result.feed_title
            self.on_post_click = res.data.result.on_post_click
            self.layout = res.data.result.layout
            self.configuration = res.data.result.configuration
            self.temp.per_slide = res.data.result.per_slide
            self.number_of_posts = res.data.result.number_of_posts
            self.number_of_rows = res.data.result.number_of_rows
            self.number_of_columns = res.data.result.number_of_columns
            self.post_spacing = self.post_spacing_options.find(spacing => spacing.value == res.data.result.post_spacing)
            self.show_likes = self.show_likes_options.find(show => show.value == res.data.result.show_likes)
            self.show_followers = self.show_followers_options.find(show => show.value == res.data.result.show_followers)
            self.allImages = res.data.result.media.data
            self.allImages.filter(image => image.hover = false)
            self.list_products = res.data.result.products
            for (let post of self.allImages) {
                if (!post.list_tags) {
                    post.list_tags = []
                }
            }
            console.log(self.allImages)
            console.log(this)
        })
    }
    ,
    methods: {
        handleShopNow(handle) {
            window.open('/products/' + handle)
        },
        redirectToInstagramUser() {
            window.open('https://instagram.com/' + this.username)
        },
        next_slide() {
            if (this.layout.includes('Grid')) {
                if (this.allImages.indexOf(this.selected_post) >= this.number_of_grid_posts - 1) {
                    this.selected_post = this.allImages[0]
                } else {
                    this.selected_post = this.allImages[this.allImages.indexOf(this.selected_post) + 1]
                }
            } else {
                if (this.allImages.indexOf(this.selected_post) >= this.number_of_posts - 1) {
                    this.selected_post = this.allImages[0]
                } else {
                    this.selected_post = this.allImages[this.allImages.indexOf(this.selected_post) + 1]
                }
            }
        },
        prev_slide() {
            if (this.layout.includes('Grid')) {
                if (this.allImages.indexOf(this.selected_post) > 0) {
                    this.selected_post = this.allImages[this.allImages.indexOf(this.selected_post) - 1]
                } else {
                    this.selected_post = this.allImages[this.number_of_grid_posts - 1]
                }
            } else {
                if (this.allImages.indexOf(this.selected_post) > 0) {
                    this.selected_post = this.allImages[this.allImages.indexOf(this.selected_post) - 1]
                } else {
                    this.selected_post = this.allImages[this.number_of_posts - 1]
                }
            }
        },
        show_post(post) {
            if (this.on_post_click.includes('pop')) {
                this.selected_post = post
                this.post_modal = true
            } else if (this.on_post_click.includes('instagram')) {
                window.open(post.permalink, '_blank')
            }
        },
    }

}

</script>
<style>
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

.post_hover {
    width: 100%;
    height: 100%;
    cursor: pointer;
    display: flex;
    text-align: center;
    align-items: center;
    justify-content: center;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 20;
    position: absolute;
    opacity: 0.5;
    background: #151515
}

.ant-modal-close-icon svg {
    margin: 20px;
}

.controls {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    width: 100%;
    margin: 10px 0px 0px 10px;
    z-index: 999;
}

.controls svg {
    font-size: 25px;
}
</style>