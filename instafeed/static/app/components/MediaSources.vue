<template>
  <div v-if="selected_content=='select_account'">
    <input type="text" v-model="new_media_source_name"/>
    <div>List facebook account</div>
    <div style="display:flex;gap: 15px;align-items: center;margin: 20px"
         v-for="account in proptemp.social_accounts.facebook_accounts">
      <input type="radio" id="option1" :value="account" v-model="selected_account">
      <div>
        <img :src="account.url_image">
      </div>
      <div>{{ account.username }}</div>
    </div>
    <button @click="createMedia()">Create</button>
  </div>
  <div id="list_media_source" v-if="selected_content=='list_media_source'">
    <button @click="addMediaSource">
      Add media source
    </button>
    <div>
      <div>List media source</div>
      <div style="display:flex;gap: 20px">
        <table class="table table-responsive table-bordered" id="table_1">
          <tr>
            <th>
              Media Source Id
            </th>
            <th>
              Media Source Name
            </th>
            <th>
              Facebook account Name
            </th>
            <th>
            </th>
            <th>
            </th>
          </tr>
          <tr v-for="source in proptemp.media_sources">
            <td>{{ source.id }}</td>
            <td>{{ source.name }}</td>
            <td>{{ source.social_account.username }}</td>
            <td>
              <div @click="editMediaSource(source)">
                <font-awesome-icon :icon="['fasr', 'pencil']"/>
              </div>
            </td>
            <td>
              <div @click="deleteMediaSource(source)">
                <font-awesome-icon :icon="['fas', 'trash-can']"/>
              </div>
            </td>
          </tr>
        </table>
      </div>
    </div>
  </div>
  <div v-if="selected_content=='select_post'">
    <div>{{ selected_source.name }}</div>
    <div>Select post</div>
    <button @click="save()">Save</button>
    <div>
      <div style="display: flex;gap: 15px;margin: 40px" v-for="post in selected_account.posts">
        <input @click="test" type="checkbox" v-model="post.select">
        <div style="width: 100px;height: 100px">
          <img style="width: 100%;
                      height: 100%" :src="post.media_url"/>
        </div>
      </div>
    </div>
  </div>

</template>
<script>
import {defineComponent} from 'vue'
import axios from 'axios'

export default defineComponent({
  name: "MediaSources",
  emits: ['createMediaSource', 'saveMediaSource'],
  props: {
    proptemp: Object
  },
  data() {
    return {
      content: ['list_media_source', 'select_account', 'select_post'],
      selected_content: 'list_media_source',
      selected_account: null,
      new_media_source_name: 'Default Name',
      selected_source: null,
    }
  }
  ,
  methods: {
    test() {
      console.log(this.list_selected_post)
    },
    selectPost() {
      console.log()
      this.selected_content = 'select_post'
    },
    selectMediaSource() {
      console.log()
      this.selected_content = 'list_media_source'
    },
    editMediaSource(source) {
      this.selected_source = source
      if (this.selected_source) {
        this.selected_account = this.proptemp.social_accounts.facebook_accounts.find(account => account.user_id == source.social_account.user_id)
        if (this.selected_account) {
          for (let post of this.selected_account.posts) {
            if (this.selected_source.posts.map(e => e.post_id).includes(post.post_id)) {
              post.select = true
            }
          }
          this.selectPost()
        }
      }
    },
    deleteMediaSource(source) {
      let self = this
      axios.post('/instafeed/delete/media_source', {media_source_id: source.id}).then((res) => {
        console.log(res)
        self.proptemp.media_sources = self.proptemp.media_sources.filter(e => e.id != source.id)
        if (res) {
          alert('Delete success')
        }
      })
    },
    addMediaSource() {
      this.selected_content = 'select_account'
    },
    createMediaSource() {
      if (this.selected_account) {
        let self = this
        this.selected_content = 'select_account'
        let params = {
          'user_id': self.selected_account.user_id,
          'name': self.new_media_source_name,
        }
        this.$emit('createMediaSource', params)
      } else {
        alert('please choose your account to select posts')
      }
    },
    save() {
      this.selected_source.posts = this.list_selected_post
      let self = this
      this.selected_content = 'select_account'
      let params = {
        'media_source_id': self.selected_source.id,
        'user_id': self.selected_account.user_id,
        'list_selected_post_id': self.list_selected_post.map(e => e.post_id)
      }
      this.$emit('saveMediaSource', params)
    },
  },
  computed: {
    list_selected_post() {
      console.log(this.list_selected_post)
      return this.selected_account.posts.filter(post => post.select == true)
    }
  },
  mounted() {
    console.log(this.proptemp)
  }
})
</script>

<style scoped>
#table_1 {
  display: table;
  width: 100%;
  left: 20px;
  top: 5px;
  column-gap: 30px;
  row-gap: 30px;
}


#table_1 th {
  text-align: left !important;
}

#table_1 td {
  text-align: left;
  font-family: 'Inter';
  font-style: normal;
  color: rgba(0, 0, 0, 0.85);
  flex: none;
  order: 0;
  flex-grow: 0;
}
</style>