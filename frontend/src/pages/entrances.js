        import {workspace} from '../workspace.js';
        import {el} from '../dom.js';

        const page = {
  "title": "入口现场勘验",
  "module": "入口设施核验",
  "caption": "入口设施核验",
  "detail": "坡道通行能力由现场见证更新，并在图签发布前再次核对。",
  "path": "/entrances",
  "columns": [
    {
      "name": "code",
      "label": "编号"
    },
    {
      "name": "park",
      "label": "口袋公园"
    },
    {
      "name": "ramp",
      "label": "坡道通行"
    },
    {
      "name": "tags",
      "label": "障碍标记"
    },
    {
      "name": "condition",
      "label": "核验状态"
    }
  ],
  "layout": "split",
  "view": "grid",
  "actions": [
    {
      "name": "inspect",
      "label": "确认入口当前状态",
      "path": "/entrances/inspect",
      "fields": [
        {
          "name": "entrance",
          "label": "入口",
          "kind": "text",
          "initial": "PK-W1"
        },
        {
          "name": "ramp",
          "label": "坡道通行",
          "kind": "bool",
          "initial": true
        }
      ],
      "help": "维护人员以现场踏勘为准更新坡道状态。",
      "roles": [
        "operator",
        "reviewer"
      ],
      "success": "已写入"
    }
  ]
};

        export const {title} = page;
        export const key = "entrances";
        export async function render(root, role) {
          await workspace(root, role, page);

        }
