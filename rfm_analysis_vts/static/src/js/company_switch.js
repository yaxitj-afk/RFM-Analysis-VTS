/** @odoo-module **/

import { rpc } from "@web/core/network/rpc";
import { SwitchCompanyMenu } from "@web/webclient/switch_company_menu/switch_company_menu";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class MySwitchCompanyMenu extends SwitchCompanyMenu {
    setup() {
    console.log("RFM Company Switch detected setup");
        super.setup();
    }
    async resetState() {
            console.log("RFM Company Switch detected is reset state",this.companySelector.selectedCompaniesIds);
            const response = await rpc("/company_switch/hook", {
            company_ids: this.companySelector.selectedCompaniesIds,
        });
        this.state.searchFilter = "";
        this.state.showFilter = this.hasLotsOfCompanies;
        this.state.visibleCompanies = this.computeVisibleCompanies();
    }

    get isSingleCompany() {
        console.log("RFM Company Switch detected is Single Call",this.companySelector.selectedCompaniesIds);

//        console.log(this.companySelector);
//        console.log(this.companySelector.selectedCompaniesIds);
//        console.log(Object.values(this.companyService.allowedCompaniesWithAncestors ?? {}));
//        const response = await rpc("/company_switch/hook", {
//            company_ids: this.companySelector.selectedCompaniesIds,
//        });
        return Object.values(this.user.allowedCompaniesWithAncestors ?? {}).length === 1;
    }
    async confirm() {
        console.log("RFM Company Switch detected confirm");

        this.dropdown.close();

        const response = await rpc("/company_switch/hook", {
            company_ids: this.companySelector.selectedCompaniesIds,
        });
        this.companySelector.apply();
        window.location.reload();

    }
}

export const mySystrayItem = {
    Component: MySwitchCompanyMenu,
};

registry.category("systray").remove("SwitchCompanyMenu");
registry.category("systray").add("SwitchCompanyMenu", mySystrayItem, { sequence: 1, force: true });
