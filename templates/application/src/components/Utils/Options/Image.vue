<template>
  <widget-options :instance="instance" @push="$emit('push')">
    <div class="form-group">
      <options-item :isHeader="true">
        <span slot="title">Image</span>
      </options-item>
      <options-item>
        <div class="mb-3 d-flex flex-column" slot="input">
          <div class="d-flex mb-1">
            <input
                class="form-control-file"
                v-scope:id.content
                :disabled="$env.state.changesLock"
                type="file"
            />
            <button class="btn btn-sm text-success mx-2" @click="upload"><i class="fas fa-upload"></i></button>
          </div>
          <div class="d-flex justify-content-between mb-1" v-if="instance.source && instance.source.file">
            <div>
              <a :href="sourceURL + '?attachment'" target="_blank" class="text-truncate mr-3">Download</a>
              <a :href="sourceURL" target="_blank" class="text-truncate">Open</a>
            </div>
            <button class="btn btn-sm text-danger mx-2" @click="remove"><i class="fas fa-trash"></i></button>
          </div>
          <div class="text-danger" v-show="error">{{ error }}</div>
        </div>
      </options-item>
      <options-item>
        <label slot="title" class="form-check-label" v-scope:for.alt>Alternative text</label>
        <input
            slot="input"
            v-scope:id.alt
            v-model="instance.alt"
            @change="$emit('push')"
            :disabled="$env.state.changesLock"
            class="form-control"
        />
        <span slot="help">This text will be displayed if we fail to obtain an image for any reason</span>
      </options-item>
    </div>
  </widget-options>
</template>

<script>
import WidgetOptions from "./_WidgetOptions";
import OptionsItem from "../Options.Item";
import $ from "jquery";

export default {
  name: "ImageOptions",
  props: {
    instance: {
      type: Object,
      required: true,
    },
  },
  components: {
    OptionsItem,
    WidgetOptions,
  },
  data() {
    return {
      error: null
    }
  },
  computed: {
    sourceURL() {
      if (this.instance.source && this.instance.source.file) {
        return this.$store.state.app.sourceURL + this.instance.source.id;
      }
      return false;
    },
  },
  methods: {
    async upload() {
      let file = $("#" + this._("content")).get(0).files[0];
      if (file !== undefined) {
        if (file.size <= this.$store.state.meta.file_size_max) {
          this.error = null;
          var data = new FormData(); //Create form data objects to facilitate file transfer to the back end
          data.append("file", file); //To add (encapsulate) a file object to a formdata object
          await this.$proxy.dispatch("uploadSource", {
            instance: this.instance,
            name: file.name,
            data,
          });
          return
        }
        return (this.error = "File is larger than 10Mb");
      }
      return (this.error = "File not selected");
    },
    remove() {
      return this.$store.dispatch("removeSource", this.instance);
    },
  }
};
</script>
