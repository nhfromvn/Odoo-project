<template>

    <div v-if="dashboard" style="width: 50%;
                                position: absolute;
                                aspect-ratio: 1 / 1;
                                overflow-x: auto;
                                top: 50%;
                                transform: translate(-50%,0%);
                                left: 50%;">
        <div style="border-bottom: solid 1px;width: 100%;
            height:10%;font-size:20px;
            padding:20px;
            font-weight: bold">
            Select Feed
        </div>
        <div class="product_row" style="display: flex; width: 100%;height: 100px ;
                        margin: 20px 0px 20px 0px;gap:10px;
                        align-items: center" v-for="feed in feeds" @click="select_feed(feed.feed_id)">
            <div>{{ feed.feed_id }}</div>
            <div>{{ feed.feed_title }}</div>
        </div>
        <button id="btn_create" @click="create_feed">CREATE NEW FEED</button>
    </div>
    <div v-else id="container">
        <div id="navBar">
            <div>
                <button id="btn_connect" style="display: flex; gap:5px" @click="connect_instagram">
                    <font-awesome-icon :icon="['fab', 'instagram']"/>
                    <p>Connect with Instagram</p>
                </button>
                <div v-if="username" style="display: flex"><p>Connected to {{ username }} with instagram</p>
                    <p style="margin: 0px 5px">|</p>
                    <a>Change account</a></div>
            </div>
            <div>
                <button id="btn_connect_fb" style="display: flex; gap:5px" @click="connect_facebook">
                    <font-awesome-icon icon="fa-brands fa-facebook-f"
                                       style="color: white"/>
                    <p>Connect with Facebook</p>
                </button>
                <div v-if="fb_username" style="display: flex"><p>Connected to {{ fb_username }} with instagram</p>
                    <p style="margin: 0px 5px">|</p>
                    <a @click="fb_logout">Log out</a></div>
            </div>
        </div>
        <div id="content">
            <div id="content-left">
                <label>
                    <b>FEED TITLE</b>
                </label>
                <input class="input_setting" v-model="feed_title"/>
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
                        <input class="input_setting" v-model="temp.per_slide" type="number" min="0">
                    </div>
                    <div>
                        <label><b>NUMBER OF POSTS</b></label>
                        <input class="input_setting" v-if="configuration=='Auto'" disabled placeholder="Auto" id="auto">
                        <input class="input_setting" v-else="" v-model="number_of_posts" type="number" min="0" max="10">
                    </div>
                </div>
                <div v-else class="line">
                    <div>
                        <label><b>NUMBER OF ROWS</b></label>
                        <input class="input_setting" v-model="number_of_rows" type="number" min="0">
                    </div>
                    <div>
                        <label><b>NUMBER OF COLUMNS</b></label>
                        <input class="input_setting" v-if="configuration=='Auto'" disabled placeholder="Auto" id="auto">
                        <input class="input_setting" v-else="" v-model="number_of_columns" type="number" min="0"
                               max="10">
                    </div>
                </div>
                <div class="line">
                    <div>
                        <label><b>SLIDER PAGES-MOBILE</b></label>
                        <input class="input_setting" v-model="slider_pages_mobile" min="0" type="number">
                    </div>
                    <div>
                        <label><b>NUMBER OF POSTS-MOBILE</b></label>
                        <input class="input_setting" v-model="number_of_post_mobile" min="0" max="10" type="number">
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
                <!--                <div class="line">-->
                <!--                    <div>-->
                <!--                        <label><b>POST TO SHOW</b></label>-->
                <!--                        <select v-model="post_to_show"></select>-->
                <!--                    </div>-->
                <!--                    <div>-->
                <!--                        <label><b>VIDEOS AUTOPLAY</b></label>-->
                <!--                        <select v-model="videos_autoplay"></select>-->
                <!--                    </div>-->
                <!--                </div>-->
                <!--                <div>-->
                <!--                    <label><b>AUTOMATIC PRODUCT FEED</b></label>-->
                <!--                    <select v-model="automatic_product_feed">-->
                <!--                        <option> hello</option>-->
                <!--                    </select>-->
                <!--                </div>-->
                <!--                <div>-->
                <!--                    <label><b>FILTER BY HASHTAGS</b></label>-->
                <!--                    <input placeholder="Leave empty to show all post"/>-->
                <!--                </div>-->
                <button id="btn_save" @click="save_feed">Save feed</button>
                                <button style="color:#0A58CA" @click="to_dashboard">Return to dashboard</button>
            </div>
            <div id="content-right">
                <label id="preview">
                    <b>PREVIEW feed:{{feed_id}}</b>
                </label>
                <hr>
                <br>
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
                </div>
                <div style="color: #707070; margin: 0px 20px">
                    <i><b>Tip:</b> Click on a post to start tagging products</i>
                </div>
            </div>
        </div>
        <Modal style="width: 70%; height: auto;"
               :footer="null"
               v-model:visible="post_modal"
               :maskClosable="false"
               @cancel="post_modal=false">
            <div id="post_modal_container" style="display: flex">
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
                    <div style="display: flex; justify-content: center; text-align: center">
                        <button @click="tagProduct(selected_post)" class="tag_product">Tag product</button>
                    </div>
                    <div v-if="selected_post.list_tags"
                         style="height: 35%; text-align: center;width:100%;margin: 20px 25px 10px 25px;">
                        <template v-for="tag in selected_post.list_tags">
                            <div style="color: rgb(0, 0, 0);
                                        font-weight: 600;
                                        line-height: 23px;
                                        font-size: 17px;
                                        margin: 15px;">{{
                                list_products.find(product => product.product_id == tag).name
                                }}
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
        <Modal style="width: 50%; height: 100%;"
               :footer="null"
               v-model:visible="tag_modal"
               :maskClosable="false"
               @cancel="tag_modal=false;this.cancel()">
            <div>
                <div style="border-bottom: solid 1px;width: 100%;
            height:10%;font-size:20px;
            padding:20px;
            font-weight: bold">
                    Add products
                </div>
                <a-input id="search_recommend_bar" v-model:value="search_recommendation"
                         placeholder="Search product by name"
                         :suffix="this.list_recommend_product.length + ' selected'"/>
            </div>

            <div class="show_product" v-if="this.list_recommend_product.length > 0">
                <div class="product" v-for="product in this.list_recommend_product" :key="product">
                    <p>
                        {{ product.name }}
                    </p>
                    <font-awesome-icon :icon="['fas', 'circle-xmark']" size="sm"
                                       @click="handleClickRecommendProduct(product.product_id)"
                                       style="height: 15px; margin-right: 10px; color: red; margin-top: 5px; width: 15px; margin-bottom: 5px"/>
                </div>
            </div>
            <hr>
            <div style="height: 50%;overflow-y:auto;">
                <div class="product_row" style="display: flex; width: 100%;height: 100px ;
                        margin: 20px 0px 20px 0px;gap:10px;
                        align-items: center" v-for="product in filteredRowsRecommend" @click="product.tag=!product.tag">
                    <div class="checkbox_container"><input class="checkbox" style="height: 10px;width: 10px"
                                                           type="checkbox"
                                                           v-model="product.tag"></div>
                    <div style="height: 100%"><img alt="product" style="height: 100%;
                      aspect-ratio: 1.4" :src="product.image_url"></div>
                    <div>{{ product.name }}</div>
                </div>
            </div>
            <div style="border-top: solid 1px;width: 100%;display: flex;
            height:10%;font-size:20px;justify-content: flex-end;gap:10px;
            padding:20px;
            font-weight: bold">
                <button style="display: flex;
                        justify-content: center;
                        align-items: center;
                        width: 70px;
                        padding: 5px;" @click="cancel">
                    Cancel
                </button>
                <button style="display: flex;
                        justify-content: center;
                        align-items: center;
                        width: 70px;
                        padding: 5px;" :disabled="list_recommend_product.length==0"
                        @click="addProductTag(selected_post)">Add
                </button>
            </div>
        </Modal>
    </div>
</template>

<script>
import axios from 'axios'
import Image_slider from "./components/image_slider.vue";
import {Modal, notification} from 'ant-design-vue'

export default {
    name: "App",
    components: {Image_slider, Modal},
    computed: {
        list_recommend_product: function () {
            return this.list_products.filter(product => product.tag == true)
        },
        filteredRowsRecommend: function () {
            var self = this;
            return this.list_products.filter(function (product) {
                return String(product.name).toLowerCase().indexOf(self.search_recommendation.toLowerCase()) > -1
            })
        },
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
            feeds: [],
            dashboard: true,
            feed_id: 0,
            shop_url: '',
            user_id: '',
            username: '',
            fb_username: '',
            // fb_status: 'unknown',
            followers_count: 0,
            search_recommendation: '',
            list_products: [],
            allImages: [],
            post_modal: false,
            tag_modal: false,
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
    },
    methods: {
        handleShopNow(handle) {
            window.open('https://' + this.shop_url + '/products/' + handle)
        },
        cancel() {
            this.tag_modal = false;
            this.list_products.filter(product => product.tag = false)
        },
        tagProduct(post) {
            this.tag_modal = true
            let current = this.allImages.find(image => image == post)
            if (current.list_tags) {
                for (let tag of current.list_tags) {
                    this.list_products.find(product => product.product_id == tag).tag = true
                }
            }
        },
        addProductTag(post) {
            let current = this.allImages.find(image => image == post)
            current.list_tags = this.list_recommend_product.map(product => {
                return product.product_id
            })
            this.cancel()
            console.log(this.allImages)
        },
        handleClickRecommendProduct(id) {
            this.list_products.find(product => product.product_id == id).tag = false
        },
        redirectToInstagramUser() {
            window.open('https://instagram.com/' + this.username)
        },
        save_feed() {
            let params = {
                feed_id: this.feed_id,
                feed: {
                    user_id: this.user_id,
                    username: this.username,
                    // fb_username: '',
                    // fb_status: 'unknown',
                    feed_title: this.feed_title,
                    post_spacing: this.post_spacing.value,
                    on_post_click: this.on_post_click,
                    layout: this.layout,
                    configuration: this.configuration,
                    number_of_posts: this.number_of_posts,
                    per_slide: this.temp.per_slide,
                    // slider_pages_mobile: this.slider_pages_mobile,
                    // number_of_post_mobile: this.number_of_posts,
                    number_of_rows: this.number_of_rows,
                    number_of_columns: this.number_of_columns,
                    show_likes: this.show_likes.value,
                    show_followers: this.show_followers.value,
                },
                posts: this.allImages
            }
            axios.post('/instafeed/save', params).then((res) => {
                if (res) {
                    alert('Save Success')
                } else {
                    alert('some thing went wrong')
                }
            })
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
        fb_logout() {
            let self = this
            window.location.href = '/instafeed/facebook/logout'
            self.fb_username = ''

        },
        connect_facebook() {
            let self = this
            window.location.href = '/instafeed/facebook/connect'
        },
        connect_instagram() {
            window.location.href = '/instafeed/connect'
        },
        create_feed() {
            let self = this
            axios.get('/instafeed/create/feed').then((res) => {
                self.feed_id = res.data.feed_id
                this.dashboard = false
            })
        },
        select_feed(id) {
            console.log(id)
            this.feed_id = id
            this.dashboard = false
            let self = this
            axios.get('/instafeed/get/shopify').then((res) => {
                self.list_products = res.data.products
                self.shop_url = res.data.shop_url
                console.log(self.list_products)
                for (let product of self.list_products) {
                    product.tag = false
                }
            })
            axios.post('/instafeed/get/data', {'feed_id': id}).then((res) => {
                console.log(res)
                self.username = res.data.result.user.username
                self.fb_username = window.fb_username
                self.user_id = res.data.result.user_id
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
                // self.allImages = res.data.media.data
                self.feed_id = res.data.result.feed_id
                console.log(self.feed_id)
                self.allImages.filter(image => image.hover = false)
                axios.post('/instafeed/get/fb-data', {'feed_id': id}).then((res) => {
                    if (res.data.result.media) {
                        self.fb_username = res.data.result.fb_username
                        self.allImages = res.data.result.media.data
                        for (let post of self.allImages) {
                            if (!post.list_tags) {
                                post.list_tags = []
                            }
                        }
                        self.followers_count = res.data.result.followers_count
                    }
                })
            })
        },
        to_dashboard() {
            this.dashboard = true
        }
    },
    mounted() {
        let self = this
        axios.get('/instafeed/select').then((res) => {
            console.log(res)
            self.feeds = res.data.feeds
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


.input_setting {
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
    display: flex;
    box-shadow: 0 0 0 1px rgba(63, 63, 68, .05), 0 1px 3px 0 rgba(63, 63, 68, .15);
    margin-bottom: 2rem;
    background-color: #ffffff;
    padding: 20px;
    gap: 30px;
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

#btn_connect_fb {
    color: #ffffff;
    align-items: center;
    flex-wrap: wrap !important;
    border-radius: 4px;
    background: rgb(0, 30, 128);
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

#btn_create {
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
@media screen and (max-width: 800px) {
  #post_modal_container{
      display: flex;
      flex-direction: column;
  }
}
.ant-modal-close-icon svg {
    margin: 20px !important;;
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

.show_product {
    display: flex;
    gap: 26px;
    flex-wrap: wrap;

}

.product {
    display: flex;
    align-items: center;
    box-sizing: border-box;
    background: #FFFFFF;
    border: 1px solid #E2E2E2;
    border-radius: 6px;
    gap: 8px;
}

.product_row {
    align-items: center;
    border-bottom: solid 1px;
    padding: 16px;
}

.product_row:hover {
    background-color: #6f726f;
    cursor: pointer;
}

.checkbox_container {
    height: 100% !important;
    padding: 20px !important;
    margin: 0px !important;
}

.checkbox {
    overflow: hidden;
    min-height: 15px;
    min-width: 15px;
    appearance: auto;
}

#search_recommend_bar {
    margin-bottom: 0px !important;
    box-sizing: border-box;
    width: 100%;
    height: auto;
    background: #FFFFFF;
    border: 1px solid #E2E2E2;
    border-radius: 6px;
}

.ant-input-affix-wrapper {
    margin: 20px 0px 10px 0px;
    padding: 10px 15px;
}
</style>