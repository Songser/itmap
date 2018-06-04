<template>
  <v-card>
    <v-card-title>
      添加节点
    </v-card-title>
    <v-card-text>
      <v-form>
        <v-layout row>
          <v-flex xs4>
            <v-subheader>图标</v-subheader>
          </v-flex>
          <v-flex xs8 mb-3>
            <v-avatar size="70" color="grey lighten-4" @click="imagecropperShow=true">
              <img :src="image" alt="avatar" v-show="image">
            </v-avatar>
            <image-cropper :width="300" :height="300" :field="field" @close='close' @cropSuccess="cropSuccess" langType="zh" v-show="imagecropperShow"></image-cropper>
          </v-flex>
        </v-layout>
        <v-layout row>
          <v-flex xs4>
            <v-subheader>图谱</v-subheader>
          </v-flex>
          <v-flex xs8>
            <v-text-field v-model="graph.name" label="" disabled></v-text-field>
          </v-flex>
        </v-layout>
        <v-layout row>
          <v-flex xs4>
            <v-subheader>上级节点</v-subheader>
          </v-flex>
          <v-flex xs8>
            <v-text-field v-model="node.name" disabled></v-text-field>
          </v-flex>
        </v-layout>
        <v-layout row>
          <v-flex xs4>
            <v-subheader>名称</v-subheader>
          </v-flex>
          <v-flex xs8>
            <v-text-field v-model="name" autofocus></v-text-field>
          </v-flex>
        </v-layout>
        <v-layout row>
          <v-flex xs4>
            <v-subheader>关系</v-subheader>
          </v-flex>
          <v-flex xs8>
            <v-text-field v-model="info"></v-text-field>
          </v-flex>
        </v-layout>
        <v-layout row>
          <v-flex xs4>
            <v-subheader>颜色</v-subheader>
          </v-flex>
          <v-flex xs8>
            <v-text-field v-model="color" type="color"></v-text-field>
          </v-flex>
        </v-layout>
        <v-layout row>
          <v-flex xs4>
            <v-subheader>大小</v-subheader>
          </v-flex>
          <v-flex xs8>
            <v-radio-group v-model="size" row>
              <v-radio label="小" value="S"></v-radio>
              <v-radio label="中" value="M"></v-radio>
              <v-radio label="大" value="L"></v-radio>
            </v-radio-group>
          </v-flex>
        </v-layout>
        <v-layout row>
          <v-flex xs4>
            <v-subheader>形状</v-subheader>
          </v-flex>
          <v-flex xs8>
            <v-radio-group v-model="shape" row>
              <v-radio label="圆形" value="circle"></v-radio>
              <v-radio label="矩形" value="roundRect"></v-radio>
              <v-radio label="三角形" value="triangle"></v-radio>
              <v-radio label="棱形" value="diamond"></v-radio>
            </v-radio-group>
          </v-flex>
        </v-layout>
        <v-layout row>
          <v-flex xs4>
            <v-subheader>描述</v-subheader>
          </v-flex>
          <v-flex xs8>
            <v-text-field v-model="desc" multi-line rows="3"></v-text-field>
          </v-flex>
        </v-layout>
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
    PanThumb
  },
  data: function() {
    console.log("fffff");
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
      action: "",
      newNodeId: 0,
      imagecropperKey: 0,
      imagecropperShow: false,
      field: "node_pic",
    };
  },
  computed: mapState({
    node: state => state.node,
    user: state => state.user,
    graph: state => state.graph,
  }),
  methods: {
    onSubmit() {
      let data = {
        graphId: this.graph.id,
        name: this.name,
        color: this.color,
        shape: this.shape,
        size: this.size,
        desc: this.desc
      };
      addNodeApi(data).then(response => {
        this.newNodeId = response.data;
        data["target_id"] = this.newNodeId;
        this.$store.commit("addNode", data);
        this.handlerUpload()
        if (this.node.name && this.name) {
          addLinkApi({
            source_id: this.node.id,
            target_id: this.newNodeId,
            graphId: this.graph.id,
            value: this.info
          }).then(response => {
            this.$store.commit("addLink", {
              source: this.node.name,
              target: this.name,
              value: this.info
            });
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
      let form = new FormData();
      form.append(this.field, data2blob(this.image, this.mime));
      form.append('fffff', 'eeeee')
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

