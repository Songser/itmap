<template>
  <v-card>
    <v-card-title>
      <p class="title">添加书籍</p>
    </v-card-title>
    <v-card-text>
      <v-form>
        <v-layout row>
          <v-flex xs2>
            封面
          </v-flex>
          <v-flex xs10>
            <v-avatar size="150" style="width:29px" color="grey lighten-4" @click="imagecropperShow=true">
              <img :src="image" alt="avatar" v-show="image">
            </v-avatar>
            <image-cropper :width="200" :height="200" :field="field" @close='close' @cropSuccess="cropSuccess" langType="zh" v-show="imagecropperShow">
            </image-cropper>
          </v-flex>
        </v-layout>
        <v-text-field v-model="title" label="标题" autofocus></v-text-field>
        <v-text-field v-model="url" label="链接"></v-text-field>
        <v-text-field v-model="author" label="作者"></v-text-field>
        <v-text-field v-model="source" label="来源"></v-text-field>
        <v-textarea v-model="desc" label="描述" multi-line rows="3"></v-textarea>
      </v-form>
    </v-card-text>
    <v-card-actions>
      <v-btn color="primary" @click="onSubmit">确定</v-btn>
      <v-btn color="primary" @click="cancle">取消</v-btn>
    </v-card-actions>
  </v-card>
</template>
<script>
import { mapState } from 'vuex'
// import UploadFile from "@/components/UploadFile";
import ImageCropper from '@/components/ImageCropper'
import data2blob from '@/utils/data2blob.js'
// import PanThumb from "@/components/PanThumb";
import {
  addBookApi,
  uploadBookPicApi
} from '@/api/book'

export default {
  name: 'add-book',
  components: {
    // UploadFile,
    ImageCropper
    // PanThumb,
  },
  data () {
    return {
      title: '',
      url: '',
      author: '',
      source: '',
      desc: '',
      image: '',
      field: 'book_pic',
      imagecropperShow: false

    }
  },
  computed: {
    ...mapState({
      node: state => state.node
    })
  },
  methods: {
    init () {
      this.title = ''
      this.url = ''
      this.author = ''
      this.source = ''
      this.desc = ''
      this.image = ''
    },
    onSubmit () {
      let data = {
        name: this.title,
        url: this.url,
        author: this.author,
        source: this.source,
        description: this.desc
      }
      addBookApi(this.node.id, data).then(response => {
        let bookId = response.data
        this.handlerUpload(bookId)
        data['id'] = bookId
        this.$root.eventHub.$emit('addArticleEvent', data)
        this.$emit('closeAddBookDialog')
        this.init()
      })
    },
    cancle () {
      this.$emit('closeAddBookDialog')
      this.init()
    },
    cropSuccess (createImgUrl, field, mime, ki) {
      this.image = createImgUrl
      this.mime = mime
    },
    handlerUpload (bookId) {
      if (!this.image) {
        return
      }
      let index = this.image.indexOf('data:image')
      if (index !== 0) {
        return
      }
      let form = new FormData()
      form.append(this.field, data2blob(this.image, this.mime))
      uploadBookPicApi(form, bookId)
    },
    close () {
      this.imagecropperShow = false
    }
  }
}
</script>
<style lang="scss" scoped>
.input-group {
  padding: 0;
}
.v-avatar img{
  border-radius: 0;
}
.panThumb {
  z-index: 100;
  height: 70px !important;
  width: 70px !important;
  border: 5px solid #ffffff;
  background-color: #fff;
  box-shadow: none !important;
  /deep/ .pan-info {
    box-shadow: none !important;
  }
}
</style>
