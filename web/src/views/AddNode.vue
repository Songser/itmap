<template>
  <v-card>
    <v-card-title>
      添加节点
    </v-card-title>
    <v-card-text>
      <v-form>
        <v-layout row>
          <v-flex xs2>
            图片
          </v-flex>
          <v-flex xs10>
            <v-avatar size="70" color="grey lighten-4" @click="imagecropperShow=true">
              <img :src="image" alt="avatar" v-show="image">
            </v-avatar>
            <image-cropper :width="300" :height="300" :field="field" @close='close' @cropSuccess="cropSuccess" langType="zh" v-show="imagecropperShow">
            </image-cropper>
          </v-flex>
        </v-layout>
        <v-text-field v-model="graph.name" label="图谱" disabled></v-text-field>
        <v-text-field v-model="node.name" label="上级节点" disabled></v-text-field>
        <v-text-field v-model="name" label="名称" autofocus></v-text-field>
        <v-text-field v-model="info" label="关系"></v-text-field>
        <!-- <v-text-field v-model="color" lebel="颜色" type="color"></v-text-field> -->
        <chrome-picker v-model="color" />
        <v-radio-group v-model="size" row>
          <v-radio label="小" value="S"></v-radio>
          <v-radio label="中" value="M"></v-radio>
          <v-radio label="大" value="L"></v-radio>
        </v-radio-group>
        <v-radio-group v-model="shape" row>
          <v-radio label="圆形" value="circle"></v-radio>
          <v-radio label="矩形" value="roundRect"></v-radio>
          <v-radio label="三角形" value="triangle"></v-radio>
          <v-radio label="棱形" value="diamond"></v-radio>
        </v-radio-group>

            <v-textarea v-model="desc" label="描述" multi-line rows="3"></v-textarea>
      </v-form>
    </v-card-text>
    <v-card-actions>
      <v-btn color="primary" @click.stop="onSubmit">确定</v-btn>
      <v-btn color="primary" @click.stop="cancle">取消</v-btn>
    </v-card-actions>
  </v-card>

</template>

<script>
import { mapState } from "vuex";
import { getToken } from "@/utils/auth";
import data2blob from "@/utils/data2blob.js";
import { Chrome } from 'vue-color'

import {
  addNodeApi,
  addLinkApi,
  getNodesApi,
  delNodeApi,
  uploadNodePicApi
} from "@/api/graph";
import UploadFile from "@/components/UploadFile";
import ImageCropper from "@/components/ImageCropper";
import PanThumb from "@/components/PanThumb";

export default {
  name: "add-node",
  components: {
    UploadFile,
    ImageCropper,
    PanThumb,
    "chrome-picker": Chrome,
  },
  data: function() {
    return {
      name: "",
      desc: "",
      info: "",
      color: "#c23531",
      size: "M",
      image: "",
      shape: "circle",
      dialogImageUrl: "",
      dialogVisible: false,
      newNodeId: 0,
      imagecropperShow: false,
      field: "node_pic"
    };
  },
  computed: mapState({
    node: state => state.node,
    user: state => state.user,
    graph: state => state.graph
  }),
  methods: {
    init() {
      this.name = "";
      this.desc = "";
      this.info = "";
      this.color = "#c23531";
      this.size = "M";
      this.image = "";
      this.shape = "circle";
      this.dialogImageUrl = "";
      this.dialogVisible = false;
      this.newNodeId = 0;
      this.imagecropperShow = false;
    },
    onSubmit() {
      console.log(this.color)
      let data = {
        graphId: this.graph.id,
        name: this.name,
        color: this.color.hex,
        shape: this.shape,
        size: this.size,
        desc: this.desc
      };
      addNodeApi(data).then(response => {
        this.newNodeId = response.data;
        data["target_id"] = this.newNodeId;
        this.handlerUpload();
        this.$root.eventHub.$emit("addNode", data);
        if (this.node.name && this.name) {
          console.log('add link')
          addLinkApi({
            source_id: this.node.id,
            target_id: this.newNodeId,
            graphId: this.graph.id,
            value: this.info
          }).then(response => {
            this.$root.eventHub.$emit("addLink", {
              source: this.node.name,
              target: this.name,
              value: this.info
            });
            this.init();
          });
        }

      });
      this.$emit("closeAddNodeDialog");
    },
    cancle() {
      this.$emit("closeAddNodeDialog");
    },
    cropSuccess(createImgUrl, field, mime, ki) {
      this.image = createImgUrl;
      this.mime = mime;
    },
    handlerUpload() {
      if (!this.image){
        return
      }
      let form = new FormData();
      form.append(this.field, data2blob(this.image, this.mime));
      uploadNodePicApi(form, this.newNodeId);
    },
    close() {
      this.imagecropperShow = false;
    }
  }
};
</script>
<style lang="scss" scoped>
.input-group {
  padding: 0;
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
