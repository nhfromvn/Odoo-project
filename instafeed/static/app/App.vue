<template>
  <div style="display: flex">
    <SideBar :is_selected="is_selected" @CustomEventChanged="get_select_id"/>
    <div id="container" class="container">
      <DashBoard :proptemp="dashboard_temp" v-if="is_selected=='dashboard'"/>
      <Integration :proptemp="integration_temp" v-if="is_selected=='integration'"/>
      <MediaSources :proptemp="media_source_temp" @createMediaSource="createMediaSource"
                    @saveMediaSource="saveMediaSource"
                    ref="media_sources_ref"
                    v-if="is_selected=='media_source'"/>
      <Widgets :proptemp="widget_temp" v-if="is_selected=='widget'" @createWidget="createWidget" @saveFeed="saveFeed"
               ref="widget_ref"/>
    </div>
  </div>

  <!--    <Loading v-if="!products||!temp.status&&is_selected!='dashboard'"/>-->
</template>

<script>
import SideBar from "./components/SideBar.vue";
import axios from 'axios'
import Integration from "./components/Integration.vue";
import DashBoard from "./components/DashBoard.vue";
import Widgets from "./components/Widgets.vue";
import MediaSources from "./components/MediaSources.vue";

export default {
  name: "App",
  components: {MediaSources, Widgets, DashBoard, Integration, SideBar},
  data() {
    return {
      is_selected: 'dashboard',
      dashboard_temp: {
        app_user: ''
      },
      integration_temp: {
        facebook_count: 0,
        instagram_count: 0,
      },
      media_source_temp: {
        social_accounts: null,
        media_sources: null,
      },
      widget_temp: {
        media_sources: [],
        products: [],
        widgets: [],

      },
    }
  },
  mounted() {
    let self = this
    axios.get('/instafeed/get/data').then((res) => {
      console.log(res)
      self.dashboard_temp.app_user = res.data.username
      self.integration_temp.facebook_count = res.data.social_accounts.facebook_accounts ? res.data.social_accounts.facebook_accounts.length : 0
      self.integration_temp.instagram_count = res.data.social_accounts.instagram_accounts ? res.data.social_accounts.instagram_accounts.length : 0
      self.media_source_temp.social_accounts = res.data.social_accounts
      self.media_source_temp.media_sources = res.data.media_sources
      self.widget_temp.media_sources = res.data.media_sources
      self.widget_temp.products = res.data.products
      self.widget_temp.widgets = res.data.widgets
      if (self.media_source_temp.social_accounts.facebook_accounts) {
        for (let account of self.media_source_temp.social_accounts.facebook_accounts) {
          account.posts.filter(post => post.select = false)
          console.log(account)
        }
      }
      if (self.widget_temp.media_sources) {
        for (let source of self.widget_temp.media_sources) {
          source.select = false
          console.log(source)
        }
      }
      console.log(self.widget_temp.products)
    })
  },
  methods: {
    get_select_id(data) {
      this.is_selected = data
    },
    createWidget(data) {
      console.log(data)
      let self = this
      axios.post('/instafeed/create/widget', data).then((res) => {
        if (self.$refs.widget_ref) {
          self.widget_temp.widgets.push(res.data.result)
          self.$refs.widget_ref.edit(res.data.result);
        }
      })
    },
    saveFeed(data) {
      let self = this
      axios.post('/instafeed/save/feed', data).then((res) => {
        if (self.$refs.widget_ref) {
          console.log(res)
          if (res.data.result.status) {
            alert('save success')
          }
          self.$refs.widget_ref.selected_content = self.$refs.widget_ref.contents[0]
          self.widget_temp.media_sources.filter(e => e.select = false)
        }
      })
    },
    createMediaSource(data) {
      let self = this
      console.log(data)
      axios.post('/instafeed/create/media_source', data).then((res) => {
        if (self.$refs.media_sources_ref) {
          self.$refs.media_sources_ref.selectPost();
          self.media_source_temp.media_sources.push(res.data.result)
          self.$refs.media_sources_ref.editMediaSource(res.data.result);
        }
      })
    },
    saveMediaSource(data) {
      let self = this
      axios.post('/instafeed/save/media_source', data).then((res) => {
        if (self.$refs.media_sources_ref) {
          self.$refs.media_sources_ref.selectMediaSource();
          let a = self.media_source_temp.media_sources.find(e => e.id == res.data.result.id)
          console.log(a)
        }
      })
    }
  }
}

</script>

<style scoped>
</style>