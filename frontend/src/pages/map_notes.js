        import {workspace} from '../workspace.js';
        import {el} from '../dom.js';

        const page = {
  "title": "现场导视图版本",
  "module": "导视图签注",
  "caption": "导视图签注",
  "detail": "签注以当前坡道通行条件为准。没有可用替代坡道时，图例只说明绕行受阻。",
  "path": "/map_notes",
  "columns": [
    {
      "name": "code",
      "label": "编号"
    },
    {
      "name": "detour",
      "label": "线路单"
    },
    {
      "name": "legend",
      "label": "导视文本"
    },
    {
      "name": "edition",
      "label": "图纸版本"
    }
  ],
  "layout": "stack",
  "view": "grid",
  "actions": [
    {
      "name": "publish_map",
      "label": "签出导视图图签",
      "path": "/map_notes/publish-map",
      "fields": [
        {
          "name": "code",
          "label": "图签编号",
          "kind": "text",
          "initial": "NOTE-11"
        },
        {
          "name": "detour",
          "label": "线路单号",
          "kind": "text",
          "initial": "DP-11"
        },
        {
          "name": "edition",
          "label": "版本标记",
          "kind": "text",
          "initial": "2026-11-24b"
        }
      ],
      "help": "复核员签出一条独立图签，文本按现场可通行条件生成。",
      "roles": [
        "reviewer"
      ],
      "success": "已写入"
    }
  ]
};

        export const {title} = page;
        export const key = "map_notes";
        export async function render(root, role) {
          await workspace(root, role, page);

        }
